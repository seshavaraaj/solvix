import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import FloodLayer

router = APIRouter(prefix="/flood-layer", tags=["flood layer"])


@router.get("", summary="List loaded flood events")
def list_events(db: Session = Depends(get_db)):
    rows = db.execute(
        select(FloodLayer.event_name, func.count(), func.min(FloodLayer.event_start),
               func.max(FloodLayer.event_end), func.min(FloodLayer.source))
        .group_by(FloodLayer.event_name)
    ).all()
    return {
        "active_event": get_settings().active_event,
        "events": [
            {"event_name": e, "polygons": n, "event_start": s, "event_end": end, "source": src}
            for e, n, s, end, src in rows
        ],
    }


@router.get("/{event}", summary="Flood extent as GeoJSON FeatureCollection (map overlay)")
def get_layer(event: str, db: Session = Depends(get_db)):
    rows = db.execute(
        select(FloodLayer.id, FloodLayer.name, FloodLayer.source, func.ST_AsGeoJSON(FloodLayer.geom, 6))
        .where(FloodLayer.event_name == event)
    ).all()
    if not rows:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No flood layer for event '{event}'")
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": fid,
                "properties": {"name": name, "source": source, "event": event},
                "geometry": json.loads(geom),
            }
            for fid, name, source, geom in rows
        ],
    }
