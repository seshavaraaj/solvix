"""PDNA-style CSV export. Field names follow the PDNA structure loosely; not an official format."""

import csv
import io

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Report

COLUMNS = [
    "report_id", "district", "taluk", "village", "asset_type", "damage_type", "severity_hint",
    "latitude", "longitude", "in_flood_extent", "confidence", "flags",
    "reported_at", "verifier", "verified_at", "approver", "approved_at",
    "status", "payment_ref", "evidence_photo_url", "synthetic",
]


def _actor_at(report: Report, to_status: str) -> tuple[str, str]:
    for h in reversed(report.history):
        if h.to_status == to_status:
            name = (h.actor.name or h.actor.username or f"user {h.actor.id}") if h.actor else ""
            return name, h.created_at.isoformat()
    return "", ""


def pdna_csv(db: Session, base_url: str, district: str | None = None) -> str:
    q = select(Report).where(Report.status.in_(("approved", "paid")))
    if district:
        q = q.where(func.lower(Report.district) == district.lower())
    reports = db.scalars(q.order_by(Report.district, Report.village, Report.created_at)).unique().all()

    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(COLUMNS)
    for r in reports:
        verifier, verified_at = _actor_at(r, "verified")
        approver, approved_at = _actor_at(r, "approved")
        writer.writerow([
            r.id, r.district or "", r.taluk or "", r.village or "", r.asset.type, r.damage_type,
            r.severity_hint or "", f"{r.lat:.6f}", f"{r.lon:.6f}",
            "" if r.in_flood_extent is None else ("yes" if r.in_flood_extent else "no"),
            r.confidence, ";".join(f["code"] for f in (r.flags or [])),
            r.created_at.isoformat(), verifier, verified_at, approver, approved_at,
            r.status, r.payment_ref or "",
            f"{base_url}/reports/{r.id}/photo" if r.photo_id else "",
            "yes" if r.synthetic else "no",
        ])
    return out.getvalue()
