"""Status changes. The only place that writes report.status."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import AuditLog, Report, StatusHistory, User, utcnow
from app.services import adapters

ALLOWED = {
    "reported": {"verified", "rejected"},
    "verified": {"approved", "rejected"},
    "approved": {"paid"},
    "rejected": set(),
    "paid": set(),
}

CITIZEN_MESSAGES = {
    "verified": "Your damage report was verified by field staff.",
    "rejected": "Your damage report was not accepted. You can raise a grievance in the app.",
    "approved": "Relief for your damage report is approved.",
    "paid": "Relief payment for your damage report is sent.",
}


def audit(db: Session, actor: User | None, action: str, entity: str, entity_id: str, detail: dict | None = None):
    db.add(AuditLog(actor_id=actor.id if actor else None, action=action, entity=entity,
                    entity_id=entity_id, detail=detail))


def transition(
    db: Session,
    report: Report,
    to_status: str,
    actor: User | None,
    note: str | None = None,
    evidence_ref: str | None = None,
) -> None:
    if to_status not in ALLOWED.get(report.status, set()):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Cannot move report from '{report.status}' to '{to_status}'",
        )
    db.add(StatusHistory(
        report_id=report.id,
        from_status=report.status,
        to_status=to_status,
        actor_id=actor.id if actor else None,
        evidence_ref=evidence_ref,
        note=note,
    ))
    report.status = to_status
    report.status_changed_at = utcnow()
    audit(db, actor, f"status:{to_status}", "report", str(report.id), {"note": note})
    if to_status in CITIZEN_MESSAGES:
        adapters.notify.send(report.reporter.phone if report.reporter else None, CITIZEN_MESSAGES[to_status])
