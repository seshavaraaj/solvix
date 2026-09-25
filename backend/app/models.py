import uuid
from datetime import datetime, timezone

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

ROLES = ("citizen", "staff", "official", "admin")
ASSET_TYPES = ("house", "hut", "cattle", "crop", "boat", "shop", "other")
DAMAGE_TYPES = ("fully_damaged", "partially_damaged", "washed_away", "submerged", "dead", "other")

# Status flow: reported -> verified | rejected -> approved -> paid
STATUSES = ("reported", "verified", "rejected", "approved", "paid")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(20), default="citizen")
    name: Mapped[str | None] = mapped_column(String(100))
    district: Mapped[str | None] = mapped_column(String(60))
    taluk: Mapped[str | None] = mapped_column(String(60))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    type: Mapped[str] = mapped_column(String(20))
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    geom = mapped_column(Geometry("POINT", srid=4326))
    village: Mapped[str | None] = mapped_column(String(80))
    ration_id: Mapped[str | None] = mapped_column(String(40))


class Report(Base):
    __tablename__ = "report"

    # Client-generated UUID doubles as the idempotency key for offline retries.
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"), index=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    damage_type: Mapped[str] = mapped_column(String(30))
    severity_hint: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)

    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    geom = mapped_column(Geometry("POINT", srid=4326))
    district: Mapped[str | None] = mapped_column(String(60), index=True)
    taluk: Mapped[str | None] = mapped_column(String(60))
    village: Mapped[str | None] = mapped_column(String(80), index=True)

    captured_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    exif_lat: Mapped[float | None] = mapped_column(Float)
    exif_lon: Mapped[float | None] = mapped_column(Float)
    exif_taken_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    photo_id: Mapped[int | None] = mapped_column(Integer)
    photo_phash: Mapped[str | None] = mapped_column(String(16), index=True)

    in_flood_extent: Mapped[bool | None] = mapped_column(Boolean)
    confidence: Mapped[int] = mapped_column(Integer, default=100)
    flags: Mapped[list] = mapped_column(JSONB, default=list)

    status: Mapped[str] = mapped_column(String(20), default="reported", index=True)
    status_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    payment_ref: Mapped[str | None] = mapped_column(String(60))
    synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    asset: Mapped[Asset] = relationship(lazy="joined")
    reporter: Mapped[User] = relationship(lazy="joined")
    history: Mapped[list["StatusHistory"]] = relationship(
        order_by="StatusHistory.id", lazy="selectin"
    )
    grievances: Mapped[list["Grievance"]] = relationship(
        order_by="Grievance.id", lazy="selectin"
    )


class StatusHistory(Base):
    """Append-only. Every status change on a report writes one row here."""

    __tablename__ = "status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("report.id"), index=True)
    from_status: Mapped[str | None] = mapped_column(String(20))
    to_status: Mapped[str] = mapped_column(String(20))
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    evidence_ref: Mapped[str | None] = mapped_column(String(200))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    actor: Mapped[User | None] = relationship(lazy="joined")


class Grievance(Base):
    __tablename__ = "grievance"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("report.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Photo(Base):
    """Photo bytes live in Postgres because Render free disks are ephemeral. See services/photostore.py."""

    __tablename__ = "photo"

    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("report.id"), index=True)
    content_type: Mapped[str] = mapped_column(String(40), default="image/jpeg")
    data: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class FloodLayer(Base):
    __tablename__ = "flood_layer"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_name: Mapped[str] = mapped_column(String(60), index=True)
    name: Mapped[str | None] = mapped_column(String(120))
    geom = mapped_column(Geometry("MULTIPOLYGON", srid=4326))
    source: Mapped[str | None] = mapped_column(String(200))
    event_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    event_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    action: Mapped[str] = mapped_column(String(40))
    entity: Mapped[str] = mapped_column(String(40))
    entity_id: Mapped[str | None] = mapped_column(String(64))
    detail: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
