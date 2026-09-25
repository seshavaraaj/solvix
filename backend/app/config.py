from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://meetpu:meetpu@localhost:5432/meetpu"
    jwt_secret: str = "change-me-in-production-use-32-plus-chars"
    jwt_ttl_hours: int = 72

    # Demo shortcut: every OTP login accepts this code. Real SMS OTP plugs in at services/adapters.py.
    mock_otp_code: str = "123456"

    # Name of the flood event whose layer drives the geo-fence and timestamp checks.
    active_event: str = "michaung-2023"

    # Verification rule tuning
    gps_mismatch_m: float = 200.0
    phash_max_distance: int = 6
    photo_max_px: int = 800

    # Hours after which a case counts as stuck in its current stage
    stuck_hours_reported: int = 48
    stuck_hours_verified: int = 72
    stuck_hours_approved: int = 168

    cors_origins: str = "*"

    @property
    def sqlalchemy_url(self) -> str:
        # Render hands out postgres:// URLs; SQLAlchemy needs the driver named.
        url = self.database_url
        for prefix in ("postgres://", "postgresql://"):
            if url.startswith(prefix):
                return "postgresql+psycopg://" + url[len(prefix):]
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
