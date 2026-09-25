import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models import ASSET_TYPES, DAMAGE_TYPES

AssetType = Literal[ASSET_TYPES]  # type: ignore[valid-type]
DamageType = Literal[DAMAGE_TYPES]  # type: ignore[valid-type]


# ---- auth ----

class OtpRequest(BaseModel):
    phone: str = Field(min_length=10, max_length=15)


class OtpVerify(BaseModel):
    phone: str = Field(min_length=10, max_length=15)
    code: str
    name: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone: str | None
    username: str | None
    role: str
    name: str | None
    district: str | None
    taluk: str | None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---- reports ----

class ReportCreate(BaseModel):
    id: uuid.UUID = Field(description="Client-generated UUID. Idempotency key for offline retries.")
    asset_type: AssetType
    damage_type: DamageType
    severity_hint: int | None = Field(default=None, ge=1, le=5)
    description: str | None = Field(default=None, max_length=2000)
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    captured_at: datetime | None = None
    district: str | None = None
    taluk: str | None = None
    village: str | None = None
    ration_id: str | None = None


class DecisionIn(BaseModel):
    decision: Literal["verified", "rejected"]
    note: str | None = None


class NoteIn(BaseModel):
    note: str | None = None


class PayIn(BaseModel):
    amount_inr: int | None = Field(default=None, ge=0)
    note: str | None = None


class GrievanceIn(BaseModel):
    text: str = Field(min_length=3, max_length=2000)


class HistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_status: str | None
    to_status: str
    actor_id: int | None
    actor_name: str | None = None
    actor_role: str | None = None
    evidence_ref: str | None
    note: str | None
    created_at: datetime


class GrievanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    status: str
    created_at: datetime


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    asset_id: int
    asset_type: str
    reporter_id: int
    reporter_name: str | None
    reporter_phone: str | None
    damage_type: str
    severity_hint: int | None
    description: str | None
    lat: float
    lon: float
    district: str | None
    taluk: str | None
    village: str | None
    captured_at: datetime | None
    exif_lat: float | None
    exif_lon: float | None
    exif_taken_at: datetime | None
    photo_url: str | None
    in_flood_extent: bool | None
    confidence: int
    flags: list[dict]
    status: str
    status_changed_at: datetime
    payment_ref: str | None
    synthetic: bool
    created_at: datetime


class ReportDetail(ReportOut):
    history: list[HistoryOut]
    grievances: list[GrievanceOut]
