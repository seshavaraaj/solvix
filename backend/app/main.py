import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import get_settings
from app.db import engine, init_db
from app.routers import auth, dashboard, export, flood, reports

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Meetpu API",
    description=(
        "Flood and cyclone damage reporting, verification and relief tracking for Tamil Nadu. "
        "Demo build: OTP, SMS, payment and Revenue integrations are mocked."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in get_settings().cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(dashboard.router)
app.include_router(export.router)
app.include_router(flood.router)


@app.get("/health", tags=["meta"])
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"ok": True}
