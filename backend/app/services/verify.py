"""Rule-based checks run on every report. Output: flags plus a 0-100 confidence.

Confidence only sorts the Staff queue. Rules never approve or reject; staff decide.
"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import FloodLayer, Report
from app.services.exif import haversine_m
from app.services.phash import hamming

PENALTY = {
    "outside_flood_extent": 40,
    "no_flood_layer": 5,
    "no_photo": 15,
    "no_exif_gps": 10,
    "gps_mismatch": 30,
    "duplicate_photo": 40,
    "outside_event_window": 20,
}


@dataclass
class RuleInput:
    lat: float
    lon: float
    in_flood_extent: bool | None
    has_photo: bool
    exif_lat: float | None
    exif_lon: float | None
    taken_at: datetime | None
    event_start: datetime | None
    event_end: datetime | None
    duplicate_of: str | None
    gps_mismatch_m: float


def evaluate(inp: RuleInput) -> tuple[int, list[dict]]:
    """Pure function: no DB access, easy to unit test."""
    flags: list[dict] = []

    if inp.in_flood_extent is None:
        flags.append({"code": "no_flood_layer", "message": "No flood layer loaded for the active event"})
    elif not inp.in_flood_extent:
        flags.append({"code": "outside_flood_extent", "message": "Location is outside the mapped flood extent"})

    if not inp.has_photo:
        flags.append({"code": "no_photo", "message": "No photo uploaded yet"})
    else:
        if inp.exif_lat is None or inp.exif_lon is None:
            flags.append({"code": "no_exif_gps", "message": "Photo has no EXIF GPS; device GPS used"})
        else:
            dist = haversine_m(inp.lat, inp.lon, inp.exif_lat, inp.exif_lon)
            if dist > inp.gps_mismatch_m:
                flags.append({
                    "code": "gps_mismatch",
                    "message": f"Photo GPS is {dist:.0f} m from reported location",
                    "distance_m": round(dist),
                })
        if inp.duplicate_of:
            flags.append({
                "code": "duplicate_photo",
                "message": "Photo matches another report",
                "ref": inp.duplicate_of,
            })

    if inp.taken_at and inp.event_start and inp.event_end:
        if not (inp.event_start <= inp.taken_at <= inp.event_end):
            flags.append({"code": "outside_event_window", "message": "Capture time is outside the event window"})

    confidence = 100 - sum(PENALTY[f["code"]] for f in flags)
    return max(0, min(100, confidence)), flags


def check_in_flood_extent(db: Session, lat: float, lon: float, event: str) -> bool | None:
    has_layer = db.scalar(select(func.count(FloodLayer.id)).where(FloodLayer.event_name == event))
    if not has_layer:
        return None
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    hit = db.scalar(
        select(FloodLayer.id)
        .where(FloodLayer.event_name == event, func.ST_Contains(FloodLayer.geom, point))
        .limit(1)
    )
    return hit is not None


def find_duplicate(db: Session, report: Report) -> str | None:
    if not report.photo_phash:
        return None
    max_d = get_settings().phash_max_distance
    rows = db.execute(
        select(Report.id, Report.photo_phash).where(
            Report.photo_phash.is_not(None), Report.id != report.id
        )
    ).all()
    for rid, ph in rows:
        if hamming(report.photo_phash, ph) <= max_d:
            return str(rid)
    return None


def run_checks(db: Session, report: Report) -> None:
    """Recompute in_flood_extent, flags and confidence in place."""
    settings = get_settings()
    report.in_flood_extent = check_in_flood_extent(db, report.lat, report.lon, settings.active_event)
    window = db.execute(
        select(func.min(FloodLayer.event_start), func.max(FloodLayer.event_end)).where(
            FloodLayer.event_name == settings.active_event
        )
    ).one()
    report.confidence, report.flags = evaluate(RuleInput(
        lat=report.lat,
        lon=report.lon,
        in_flood_extent=report.in_flood_extent,
        has_photo=report.photo_id is not None,
        exif_lat=report.exif_lat,
        exif_lon=report.exif_lon,
        taken_at=report.exif_taken_at or report.captured_at,
        event_start=window[0],
        event_end=window[1],
        duplicate_of=find_duplicate(db, report),
        gps_mismatch_m=settings.gps_mismatch_m,
    ))
