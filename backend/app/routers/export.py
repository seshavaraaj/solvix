from datetime import date

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.auth import require_roles
from app.db import get_db
from app.models import User
from app.services.export import pdna_csv
from app.services.workflow import audit

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/pdna", summary="PDNA-style CSV of approved and paid cases with evidence links")
def export_pdna(
    request: Request,
    district: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("official")),
):
    base_url = str(request.base_url).rstrip("/")
    body = pdna_csv(db, base_url, district)
    audit(db, user, "export", "pdna", district or "all")
    db.commit()
    name = f"meetpu-pdna-{(district or 'all').lower().replace(' ', '-')}-{date.today().isoformat()}.csv"
    return Response(
        content="﻿" + body,  # BOM so Excel opens Tamil text as UTF-8
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
