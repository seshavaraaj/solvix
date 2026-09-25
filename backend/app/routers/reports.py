import uuid
from datetime import timezone

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth import current_user, require_roles
from app.db import get_db
from app.models import STATUSES, Asset, Grievance, Report, StatusHistory, User
from app.schemas import (
    DecisionIn,
    GrievanceIn,
    GrievanceOut,
    HistoryOut,
    NoteIn,
    PayIn,
    ReportCreate,
    ReportDetail,
    ReportOut,
)
from app.services import adapters
from app.services.exif import read_exif
from app.services.phash import phash_bytes
from app.services.photostore import DbPhotoStore
from app.services.verify import run_checks
from app.services.workflow import audit, transition

router = APIRouter(tags=["reports"])

MAX_PHOTO_BYTES = 15 * 1024 * 1024


def to_out(r: Report) -> ReportOut:
    return ReportOut(
        id=r.id,
        asset_id=r.asset_id,
        asset_type=r.asset.type,
        reporter_id=r.reporter_id,
        reporter_name=r.reporter.name if r.reporter else None,
        reporter_phone=r.reporter.phone if r.reporter else None,
        damage_type=r.damage_type,
        severity_hint=r.severity_hint,
        description=r.description,
        lat=r.lat,
        lon=r.lon,
        district=r.district,
        taluk=r.taluk,
        village=r.village,
        captured_at=r.captured_at,
        exif_lat=r.exif_lat,
        exif_lon=r.exif_lon,
        exif_taken_at=r.exif_taken_at,
        photo_url=f"/reports/{r.id}/photo" if r.photo_id else None,
        in_flood_extent=r.in_flood_extent,
        confidence=r.confidence,
        flags=r.flags or [],
        status=r.status,
        status_changed_at=r.status_changed_at,
        payment_ref=r.payment_ref,
        synthetic=r.synthetic,
        created_at=r.created_at,
    )


def to_detail(r: Report) -> ReportDetail:
    history = [
        HistoryOut.model_validate(h).model_copy(update={
            "actor_name": (h.actor.name or h.actor.username) if h.actor else None,
            "actor_role": h.actor.role if h.actor else None,
        })
        for h in r.history
    ]
    return ReportDetail(
        **to_out(r).model_dump(),
        history=history,
        grievances=[GrievanceOut.model_validate(g) for g in r.grievances],
    )


def _get_report(db: Session, report_id: uuid.UUID) -> Report:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Report not found")
    return report


def _point(lat: float, lon: float):
    return func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)


@router.post("/reports", response_model=ReportDetail, summary="Create a damage report (idempotent on client UUID)")
def create_report(
    body: ReportCreate,
    response: Response,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("citizen", "staff")),
):
    existing = db.get(Report, body.id)
    if existing is not None:
        if existing.reporter_id != user.id:
            raise HTTPException(status.HTTP_409_CONFLICT, "Report id already used")
        # Offline retry of the same report: return it unchanged, create nothing.
        response.status_code = status.HTTP_200_OK
        return to_detail(existing)

    asset = Asset(
        owner_user_id=user.id,
        type=body.asset_type,
        lat=body.lat,
        lon=body.lon,
        geom=_point(body.lat, body.lon),
        village=body.village,
        ration_id=body.ration_id,
    )
    db.add(asset)
    db.flush()

    captured = body.captured_at
    if captured is not None and captured.tzinfo is None:
        captured = captured.replace(tzinfo=timezone.utc)

    report = Report(
        id=body.id,
        asset_id=asset.id,
        reporter_id=user.id,
        damage_type=body.damage_type,
        severity_hint=body.severity_hint,
        description=body.description,
        lat=body.lat,
        lon=body.lon,
        geom=_point(body.lat, body.lon),
        district=body.district or user.district,
        taluk=body.taluk or user.taluk,
        village=body.village,
        captured_at=captured,
        status="reported",
        flags=[],
    )
    db.add(report)
    db.flush()
    db.add(StatusHistory(report_id=report.id, from_status=None, to_status="reported",
                         actor_id=user.id, note="Report submitted"))
    run_checks(db, report)
    audit(db, user, "create", "report", str(report.id))
    db.commit()
    db.refresh(report)
    response.status_code = status.HTTP_201_CREATED
    return to_detail(report)


@router.post("/reports/{report_id}/photo", response_model=ReportDetail, summary="Upload or replace the report photo")
async def upload_photo(
    report_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("citizen", "staff")),
):
    report = _get_report(db, report_id)
    if report.reporter_id != user.id and user.role not in ("staff", "admin"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your report")
    raw = await file.read()
    if len(raw) > MAX_PHOTO_BYTES:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "Photo too large")
    try:
        # EXIF and hash come from the original bytes; the stored copy is resized and stripped.
        exif = read_exif(raw)
        report.photo_phash = phash_bytes(raw)
        report.photo_id = DbPhotoStore(db).put(report.id, raw)
    except Exception:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "File is not a readable image")
    report.exif_lat, report.exif_lon, report.exif_taken_at = exif.lat, exif.lon, exif.taken_at
    run_checks(db, report)
    audit(db, user, "photo", "report", str(report.id), {"photo_id": report.photo_id})
    db.commit()
    db.refresh(report)
    return to_detail(report)


@router.get("/reports/{report_id}/photo", summary="Evidence photo (URL contains the unguessable report UUID)")
def get_photo(report_id: uuid.UUID, db: Session = Depends(get_db)):
    report = _get_report(db, report_id)
    if report.photo_id is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No photo")
    found = DbPhotoStore(db).get(report.photo_id)
    if found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No photo")
    data, content_type = found
    return Response(content=data, media_type=content_type,
                    headers={"Cache-Control": "private, max-age=86400"})


@router.get("/reports", response_model=list[ReportOut], summary="Queue and map data")
def list_reports(
    status_: str | None = Query(None, alias="status", description="Comma list, e.g. reported,verified"),
    district: str | None = None,
    taluk: str | None = None,
    village: str | None = None,
    bbox: str | None = Query(None, description="minLon,minLat,maxLon,maxLat"),
    flagged: bool | None = Query(None, description="true: only reports with flags"),
    sort: str = Query("confidence", pattern="^(confidence|newest|oldest)$"),
    limit: int = Query(500, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("staff", "official")),
):
    q = select(Report)
    if status_:
        wanted = [s.strip() for s in status_.split(",") if s.strip()]
        bad = [s for s in wanted if s not in STATUSES]
        if bad:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Unknown status: {', '.join(bad)}")
        q = q.where(Report.status.in_(wanted))
    if district:
        q = q.where(func.lower(Report.district) == district.lower())
    if taluk:
        q = q.where(func.lower(Report.taluk) == taluk.lower())
    if village:
        q = q.where(func.lower(Report.village) == village.lower())
    if bbox:
        try:
            min_lon, min_lat, max_lon, max_lat = (float(v) for v in bbox.split(","))
        except ValueError:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "bbox must be minLon,minLat,maxLon,maxLat")
        q = q.where(func.ST_Intersects(Report.geom, func.ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)))
    if flagged is True:
        q = q.where(func.jsonb_array_length(Report.flags) > 0)
    elif flagged is False:
        q = q.where(func.jsonb_array_length(Report.flags) == 0)

    order = {
        # Lowest confidence first: those need the closest look.
        "confidence": (Report.confidence.asc(), Report.created_at.asc()),
        "newest": (Report.created_at.desc(),),
        "oldest": (Report.created_at.asc(),),
    }[sort]
    rows = db.scalars(q.order_by(*order).limit(limit).offset(offset)).unique().all()
    return [to_out(r) for r in rows]


@router.get("/reports/{report_id}", response_model=ReportDetail)
def get_report(report_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(current_user)):
    report = _get_report(db, report_id)
    if user.role == "citizen" and report.reporter_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your report")
    return to_detail(report)


@router.post("/reports/{report_id}/verify", response_model=ReportDetail, summary="Staff: confirm or reject")
def verify_report(
    report_id: uuid.UUID,
    body: DecisionIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("staff")),
):
    report = _get_report(db, report_id)
    if body.decision == "rejected" and not body.note:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "A note is required to reject")
    transition(db, report, body.decision, user, note=body.note,
               evidence_ref=f"/reports/{report.id}/photo" if report.photo_id else None)
    db.commit()
    db.refresh(report)
    return to_detail(report)


@router.post("/reports/{report_id}/approve", response_model=ReportDetail, summary="Official: approve relief")
def approve_report(
    report_id: uuid.UUID,
    body: NoteIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("official")),
):
    report = _get_report(db, report_id)
    transition(db, report, "approved", user, note=body.note)
    db.commit()
    db.refresh(report)
    return to_detail(report)


@router.post("/reports/{report_id}/reject", response_model=ReportDetail, summary="Official: reject a verified report")
def reject_report(
    report_id: uuid.UUID,
    body: NoteIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("official")),
):
    report = _get_report(db, report_id)
    if not body.note:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "A note is required to reject")
    transition(db, report, "rejected", user, note=body.note)
    db.commit()
    db.refresh(report)
    return to_detail(report)


@router.post("/reports/{report_id}/pay", response_model=ReportDetail, summary="Official: mock payment (status only)")
def pay_report(
    report_id: uuid.UUID,
    body: PayIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("official")),
):
    report = _get_report(db, report_id)
    if report.status != "approved":
        raise HTTPException(status.HTTP_409_CONFLICT, f"Cannot pay a report in status '{report.status}'")
    report.payment_ref = adapters.payment.pay(report.id, body.amount_inr)
    transition(db, report, "paid", user, note=body.note or "Mock payment", evidence_ref=report.payment_ref)
    db.commit()
    db.refresh(report)
    return to_detail(report)


@router.post("/reports/{report_id}/grievance", response_model=GrievanceOut, status_code=201)
def raise_grievance(
    report_id: uuid.UUID,
    body: GrievanceIn,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("citizen")),
):
    report = _get_report(db, report_id)
    if report.reporter_id != user.id and user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your report")
    grievance = Grievance(report_id=report.id, user_id=user.id, text=body.text)
    db.add(grievance)
    db.flush()
    audit(db, user, "grievance", "report", str(report.id), {"grievance_id": grievance.id})
    db.commit()
    return grievance


@router.get("/me/reports", response_model=list[ReportDetail], summary="Citizen: my reports with status timeline")
def my_reports(db: Session = Depends(get_db), user: User = Depends(current_user)):
    rows = db.scalars(
        select(Report).where(Report.reporter_id == user.id).order_by(Report.created_at.desc())
    ).unique().all()
    return [to_detail(r) for r in rows]
