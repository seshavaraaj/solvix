from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth import require_roles
from app.config import get_settings
from app.db import get_db
from app.models import STATUSES, Grievance, Report, User, utcnow

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _thresholds() -> dict[str, int]:
    s = get_settings()
    return {
        "reported": s.stuck_hours_reported,
        "verified": s.stuck_hours_verified,
        "approved": s.stuck_hours_approved,
    }


@router.get("/stuck", summary="Cases per stage, per district and village, with age")
def stuck(
    district: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("official")),
):
    thresholds = _thresholds()
    q = select(Report.id, Report.status, Report.district, Report.village, Report.status_changed_at)
    if district:
        q = q.where(func.lower(Report.district) == district.lower())
    now = utcnow()

    by_status = {s: {"status": s, "count": 0, "stuck": 0, "oldest_hours": 0.0} for s in STATUSES}
    by_area: dict[tuple, dict] = defaultdict(lambda: {"count": 0, "stuck": 0, "oldest_hours": 0.0})
    stuck_cases = []

    for rid, status, dist, village, changed in db.execute(q):
        age = (now - changed).total_seconds() / 3600
        limit = thresholds.get(status)
        is_stuck = limit is not None and age > limit

        row = by_status[status]
        row["count"] += 1
        row["stuck"] += is_stuck
        row["oldest_hours"] = max(row["oldest_hours"], round(age, 1))

        area = by_area[(dist or "Unknown", village or "Unknown", status)]
        area["count"] += 1
        area["stuck"] += is_stuck
        area["oldest_hours"] = max(area["oldest_hours"], round(age, 1))

        if is_stuck:
            stuck_cases.append({
                "id": str(rid), "status": status, "district": dist, "village": village,
                "age_hours": round(age, 1), "limit_hours": limit,
            })

    stuck_cases.sort(key=lambda c: c["age_hours"] / c["limit_hours"], reverse=True)
    return {
        "thresholds_hours": thresholds,
        "by_status": list(by_status.values()),
        "by_area": [
            {"district": d, "village": v, "status": s, **vals}
            for (d, v, s), vals in sorted(by_area.items())
        ],
        "stuck_cases": stuck_cases[:100],
    }


@router.get("/summary", summary="Headline counts for the portal")
def summary(db: Session = Depends(get_db), _: User = Depends(require_roles("official"))):
    status_counts = dict(db.execute(select(Report.status, func.count()).group_by(Report.status)).all())
    flood_counts = dict(
        db.execute(select(Report.in_flood_extent, func.count()).group_by(Report.in_flood_extent)).all()
    )
    flagged = db.scalar(select(func.count()).where(func.jsonb_array_length(Report.flags) > 0))
    open_grievances = db.scalar(select(func.count()).select_from(Grievance).where(Grievance.status == "open"))
    return {
        "total": sum(status_counts.values()),
        "by_status": {s: status_counts.get(s, 0) for s in STATUSES},
        "in_flood_extent": flood_counts.get(True, 0),
        "outside_flood_extent": flood_counts.get(False, 0),
        "flagged": flagged or 0,
        "open_grievances": open_grievances or 0,
    }
