from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import check_password, current_user, issue_token
from app.config import get_settings
from app.db import get_db
from app.models import User
from app.schemas import LoginRequest, OtpRequest, OtpVerify, TokenOut, UserOut
from app.services import adapters
from app.services.workflow import audit

router = APIRouter(prefix="/auth", tags=["auth"])


def _normalize_phone(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    return digits[-10:]


@router.post("/otp", summary="Request OTP (mock: no SMS sent)")
def request_otp(body: OtpRequest):
    adapters.otp.send(_normalize_phone(body.phone))
    return {"sent": True, "mock": True, "hint": "Demo build: use the fixed demo OTP code"}


@router.post("/verify", response_model=TokenOut, summary="Verify OTP and get a JWT (citizen or staff)")
def verify_otp(body: OtpVerify, db: Session = Depends(get_db)):
    if body.code != get_settings().mock_otp_code:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong OTP")
    phone = _normalize_phone(body.phone)
    user = db.scalar(select(User).where(User.phone == phone))
    if user is None:
        # Unknown numbers sign up as citizens. Staff numbers are pre-registered by the seed script.
        user = User(phone=phone, role="citizen", name=body.name)
        db.add(user)
        db.flush()
        audit(db, user, "signup", "user", str(user.id))
    elif body.name and not user.name:
        user.name = body.name
    db.commit()
    return TokenOut(access_token=issue_token(user), user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenOut, summary="Username/password login (management portal)")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None or not check_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")
    if user.role not in ("official", "admin"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Portal login is for officials only")
    return TokenOut(access_token=issue_token(user), user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user
