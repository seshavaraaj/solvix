# Development Solution: Meetpu (மீட்பு) (24-hour hackathon build)

Product name: **Meetpu** (Tamil for "recovery, rescue"). Tagline: "Satellites show where the water was. We show who lost what."

| Field | Value |
|---|---|
| Prepared | 2026-09-25 |
| Based on | `.reports/solution/proposed-solution (1).md` |
| Audience | Solvix'26 hackathon dev team (2-3 people) |
| Time box | 24 hours |
| Scope | Software only; floods and cyclones in Tamil Nadu |

## 1. Decisions

| Area | Decision |
|---|---|
| Staff app | Flutter, real (offline queue, verification, capture) |
| User app | Flutter, thin: report damage and view status timeline only |
| Management portal | React + MapLibre, real (map, approval queue, stuck cases, export) |
| Backend | FastAPI, PostgreSQL + PostGIS, S3-compatible photo storage |
| Auth | Mock OTP (fixed code) for User and Staff; simple role login for Management. State this openly in the demo |
| Geo | Prebaked Michaung (Chennai) or Fengal (Cuddalore) inundation GeoJSON; point-in-polygon check in PostGIS. No live Earth Engine |
| Verification | Rules only: geo-fence, EXIF/GPS match, perceptual photo hash. No AI |
| Hosting | Cloud (Render, Railway or Supabase) plus APK on team phones |
| Mock | Payment (status change only), SMS/WhatsApp (logged stub), Revenue/TNeGA/PMFBY (adapter stubs) |
| Skip | Crop pre-screen (show as roadmap slide), AI triage, real OTP, Sentinel-1 |

## 2. Scope

| Priority | Item |
|---|---|
| P0 (must demo) | User report with photo and GPS; Staff verification queue; PostGIS record with status history; inundation check; Management map and approval; status timeline in User app |
| P1 | Grievance from status screen; stuck-case dashboard; PDNA-style CSV/PDF export with evidence links; Tamil and English strings |
| P2 (only if time) | Offline sync polish, audit log view, role levels (district, taluk) |
| Cut | Crop pre-screen, AI, real notifications, real payment |

## 3. Architecture

```
User app (Flutter) ─┐
Staff app (Flutter) ─┼─ HTTPS/JSON ─ FastAPI ─┬─ PostgreSQL + PostGIS
Management (React) ─┘                         ├─ Object storage (photos)
                                              └─ Adapter stubs (payment, SMS, Revenue)
```

One shared API. Clients never talk to the database or storage directly, except photo upload through presigned URLs or a multipart endpoint.

## 4. Data model

| Table | Key fields |
|---|---|
| user | id, phone, role (citizen, staff, official, admin), district, taluk, name |
| asset | id, owner_user_id, type (house, hut, cattle, crop), geom (Point), village, ration_id |
| report | id (client UUID, idempotency key), asset_id, reporter_id, damage_type, severity_hint, geom, captured_at, exif_gps, photo_url, photo_phash, in_flood_extent (bool), confidence (0-100), status |
| status_history | id, report_id, from_status, to_status, actor_id, evidence_ref, note, created_at (append-only) |
| grievance | id, report_id, text, status, created_at |
| flood_layer | id, event_name, geom (MultiPolygon), source |
| audit_log | id, actor_id, action, entity, entity_id, created_at |

Status flow: `reported` → `verified` or `rejected` → `approved` → `paid`. Every change writes a `status_history` row. Never update in place without one.

## 5. API surface

| Endpoint | Purpose | Caller |
|---|---|---|
| `POST /auth/otp`, `POST /auth/verify` | Mock OTP login, returns JWT | User, Staff |
| `POST /auth/login` | Role login | Management |
| `POST /reports` | Create report (idempotent on client UUID); runs auto checks | User, Staff |
| `POST /reports/{id}/photo` | Photo upload | User, Staff |
| `GET /reports?status=&area=&bbox=` | Queue and map data | Staff, Management |
| `POST /reports/{id}/verify` | Confirm or reject with note | Staff |
| `POST /reports/{id}/approve` | Approve relief | Management |
| `POST /reports/{id}/pay` | Mock payment, status change only | Management |
| `GET /me/reports` | Citizen status timeline | User |
| `POST /reports/{id}/grievance` | Raise grievance | User |
| `GET /dashboard/stuck` | Cases per stage, per village and district, age | Management |
| `GET /export/pdna?district=` | CSV/PDF with evidence trail | Management |
| `GET /flood-layer/{event}` | GeoJSON for map overlay | Management, Staff |

## 6. Verification rules

Run on `POST /reports`. Output: flags plus a confidence score used only to sort the Staff queue.

1. **Geo-fence:** `ST_Contains(flood_layer.geom, report.geom)` sets `in_flood_extent`.
2. **EXIF/GPS match:** distance between EXIF GPS and submitted GPS over 200 m lowers confidence. Missing EXIF lowers it slightly and adds a flag.
3. **Duplicate photo:** perceptual hash (pHash) within a small Hamming distance of an existing report flags a duplicate.
4. **Timestamp sanity:** capture time outside the event window lowers confidence.

Staff decide. Rules never auto-approve or auto-reject.

## 7. Offline-first design (Staff and User apps)

- Local SQLite (Drift) table `pending_reports` with client UUID, payload and photo path.
- Sync worker retries with backoff when network returns. The server treats the client UUID as an idempotency key, so retries create no duplicates.
- Status for pending items shows "waiting to sync" in the UI.
- Read cache: last fetched queue and timeline stay viewable offline.
- Tamil and English via Flutter `intl`; bundle a Tamil-capable font (for example Noto Sans Tamil) so text renders on all phones.

## 8. Team split and 24-hour timeline

Roles for 3 people. With 2 people, dev B takes the User app after the Staff app, and dev C takes the backend export.

| Dev | Owns |
|---|---|
| A | FastAPI, PostGIS schema, verification rules, seed script, cloud deploy |
| B | Flutter Staff app, then User app |
| C | React Management portal, export, demo data and script |

| Hours | A (backend) | B (Flutter) | C (React) |
|---|---|---|---|
| 0-2 | Repo, docker-compose, schema, PostGIS, load flood GeoJSON | Flutter project, i18n, mock login | React project, MapLibre, flood layer overlay from static file |
| 2-6 | Reports API, photo upload, auto checks, status history | Report capture (photo, GPS, EXIF) and local queue | Map of reports, filters, login page |
| 6-10 | Verify, approve, pay endpoints, JWT roles | Staff queue and verify screen | Approval queue and case detail with evidence |
| 10-14 | Stuck dashboard API, grievance API, deploy to cloud | Sync worker, offline behaviour | Stuck-case dashboard, status history view |
| 14-18 | Export endpoint, adapter stubs | User app: report and status timeline | Export button, polish |
| 18-21 | Seed synthetic reports, fix bugs | Build APK, test on real phones | UI polish, Tamil strings check |
| 21-24 | Freeze. Rehearse demo, backup video, deploy check | Same | Same |

Rule: no new features after hour 18. Record a backup demo video by hour 22.

## 9. Demo data and script

- Seed 40-60 synthetic reports inside and outside the chosen inundation polygon, in mixed statuses, with 2-3 duplicates and 2-3 GPS mismatches.
- Demo path (about 3 minutes): citizen reports damage on phone (offline, then reconnect) → report appears in Staff queue with flags → staff verify on site → official approves on map → citizen phone shows "approved" → official opens stuck-case view → export PDNA report.
- Label everything synthetic and state which integrations are mocked.

## 10. PDNA-style export

- CSV with one row per approved case: district, taluk, village, asset type, damage type, coordinates, in_flood_extent, verifier, verified_at, approver, approved_at, evidence photo URL.
- Optional PDF summary with counts per district and a sample of evidence photos.
- Note that field names follow the PDNA structure loosely; say it is not an official format.

## 11. Testing checklist

- Create report offline on a real phone, reconnect, confirm exactly one record on the server.
- Report inside and outside polygon gets the correct flag.
- Same photo submitted twice gets the duplicate flag.
- Status history shows actor and time for each change.
- Tamil text renders on the Staff and User apps on the demo phones.
- Management portal loads over venue Wi-Fi and over mobile data.
- Fresh deploy from scratch works from the README.

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Venue Wi-Fi fails during demo | Backup demo video; local docker-compose fallback on a laptop; mobile hotspot |
| Cloud cold starts (free tiers) | Ping the service before the demo; use a paid or always-on tier for the day |
| Flutter APK build or signing issues | Build a debug APK at hour 6, not hour 20 |
| Camera plugin strips EXIF | Read EXIF from the original file before compression; fall back to device GPS and flag "no EXIF" |
| Tamil font rendering | Bundle the font; test on hour 2 |
| Scope creep | P0 list is the only hard target; freeze at hour 18 |
| Mock auth looks weak to judges | State it as a demo shortcut; show OTP integration point in the adapter layer |

## 13. Resolved decisions

| Question | Answer |
|---|---|
| Inundation layer | User is sourcing it. Candidates: Bhuvan/NDEM (NRSC), Copernicus EMS Rapid Mapping, or self-derived Sentinel-1 via Earth Engine or ASF. Fallback after 30 minutes: hand-drawn polygon in geojson.io, labelled as a demo layer |
| Database host | Render Postgres with `CREATE EXTENSION postgis;` |
| Photo storage | Store photos in a Postgres `bytea` column (resized to about 800 px) behind a `PhotoStore` interface. Render free web disks are ephemeral, so files on disk would vanish on redeploy. Swap to R2 or S3 later without API change |
| Who codes | Claude writes the code; the user runs, tests and presents |
| Devices | Android only |
| Backup demo video | Allowed |
| Crop pre-screen | Not built. Add one "Next steps" slide: Sentinel-1 flood duration against crop calendar per survey number, decision support only |

## 14. Repository layout

```
solvix/
  backend/            FastAPI app
    app/main.py, models.py, schemas.py, routers/, services/(verify.py, photostore.py, export.py)
    seed/             flood.geojson, seed.py
    Dockerfile, requirements.txt
  management-web/     React + Vite + MapLibre
  mobile/             Flutter (one app, role chosen at login: citizen or staff)
  docs/               README, demo script
  render.yaml         Render blueprint (web service + Postgres)
```

Decision: one Flutter app with two roles instead of two apps. It halves the build and APK work. The User screens (report, timeline) and Staff screens (queue, verify) live in the same codebase behind role routing.

## 15. Build order (Claude codes, user tests)

Each step ends with something the user can run or click.

1. **Backend skeleton.** Schema, PostGIS, `flood_layer` load, mock auth, JWT roles. Check: `/docs` (Swagger) opens locally.
2. **Reports and rules.** `POST /reports`, photo store, geo-fence, EXIF/pHash checks, status history. Check: post a sample report with curl, see flags.
3. **Verify, approve, pay, grievance, stuck, export endpoints.** Check: full lifecycle through Swagger.
4. **Seed script.** 40-60 synthetic reports.
5. **Management web.** Login, map with flood overlay, approval queue, case detail, stuck dashboard, export button.
6. **Deploy backend and DB to Render.** Check: public Swagger URL.
7. **Flutter app.** Login, report capture, local queue and sync, timeline (User); queue and verify (Staff); Tamil and English.
8. **Build debug APK early.** Install on a phone, test against the Render URL.
9. **Polish, demo script, backup video, Next-steps slide.**

User tasks: install Flutter SDK, Android Studio and Node; create the Render account; deliver the flood GeoJSON; test on the phone.

## 16. Remaining questions

1. Is Flutter SDK plus Android Studio installed, with a working Android device or emulator?
2. Render account created (free tier is enough)?
3. Is a Tamil-English UI text list needed from you, or should Claude write the Tamil strings (native review recommended)?
