# Meetpu API (FastAPI + PostGIS)

Backend for Meetpu: damage reports, rule-based verification, status workflow, stuck-case dashboard and PDNA-style export.

Demo build. OTP, SMS, payment and Revenue/TNeGA/PMFBY integrations are mocked in `app/services/adapters.py`. All seeded reports are synthetic.

## Run locally

Needs Python 3.12+ and a Postgres database with PostGIS available.

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate          # Windows; use .venv/bin/activate on macOS/Linux
pip install -r requirements-dev.txt
cp .env.example .env            # set DATABASE_URL
python -m seed.seed             # tables, flood layer, users, 50 synthetic reports
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for Swagger.

Database options:

- Docker: `docker compose up --build` from the repo root starts PostGIS and the API together.
- Render: paste the database's External Database URL into `DATABASE_URL`.

## Demo logins

| Who | How | Credentials |
|---|---|---|
| Citizen | `POST /auth/otp`, then `POST /auth/verify` | any 10-digit phone (demo: 9000000000), OTP `123456` |
| Staff (VAO) | same OTP flow | 9800000001 (Chennai) or 9800000002 (Chengalpattu), OTP `123456` |
| Official | `POST /auth/login` | `collector` / `meetpu123` |
| Admin | `POST /auth/login` | `admin` / `meetpu123` |

Swagger: call a login endpoint, copy `access_token`, click **Authorize**.

## Status flow

`reported` → `verified` or `rejected` (staff) → `approved` or `rejected` (official) → `paid` (official, mock).
Every change appends a `status_history` row with actor, time and note.

## Verification rules (`app/services/verify.py`)

Run on report creation and on photo upload. Confidence (0-100) only sorts the staff queue. Rules never approve or reject.

| Flag | Penalty | Check |
|---|---|---|
| `outside_flood_extent` | 40 | PostGIS `ST_Contains` against the active event's flood layer |
| `gps_mismatch` | 30 | EXIF GPS over 200 m from reported GPS |
| `duplicate_photo` | 40 | pHash Hamming distance at most 6 from another report's photo |
| `outside_event_window` | 20 | Capture time outside the flood layer's event window |
| `no_photo` | 15 | No photo uploaded yet |
| `no_exif_gps` | 10 | Photo has no EXIF GPS |
| `no_flood_layer` | 5 | No flood layer loaded |

## Flood layer

`seed/flood.geojson` is a hand-drawn demo approximation of Cyclone Michaung inundation in Chennai. It is not an official product. Load a real layer with:

```bash
python -m seed.seed --flood path/to/extent.geojson --source "Bhuvan/NDEM, 2023-12-05"
```

The event window defaults to now ± 14 days so that live demo reports pass the time check. Change it with `--window-days`.

## Tests

```bash
pytest                          # unit tests for rules, pHash, EXIF (no database)
python -m scripts.smoke         # full lifecycle against a running API
python -m scripts.smoke https://<your-render-url>
```

## Deploy (Render)

`render.yaml` at the repo root defines the Postgres database and the web service. In Render: **New > Blueprint** and select this repo. The start command runs the seed (idempotent) and then uvicorn.
