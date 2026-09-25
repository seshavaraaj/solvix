"""Photo storage behind one interface. Today: Postgres bytea. Later: R2/S3 without API change."""

import io
import uuid
from typing import Protocol

from PIL import Image, ImageOps
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Photo


class PhotoStore(Protocol):
    def put(self, report_id: uuid.UUID, raw: bytes) -> int: ...
    def get(self, photo_id: int) -> tuple[bytes, str] | None: ...


def shrink_jpeg(raw: bytes, max_px: int) -> bytes:
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
    img = img.convert("RGB")
    img.thumbnail((max_px, max_px))
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=80, optimize=True)
    return out.getvalue()


class DbPhotoStore:
    def __init__(self, db: Session):
        self.db = db

    def put(self, report_id: uuid.UUID, raw: bytes) -> int:
        photo = Photo(report_id=report_id, data=shrink_jpeg(raw, get_settings().photo_max_px))
        self.db.add(photo)
        self.db.flush()
        return photo.id

    def get(self, photo_id: int) -> tuple[bytes, str] | None:
        photo = self.db.get(Photo, photo_id)
        return (photo.data, photo.content_type) if photo else None
