"""Seed demo data: flood layer, users and 50 SYNTHETIC reports.

Run from backend/:  python -m seed.seed            (first time)
                    python -m seed.seed --reset    (wipe synthetic reports and reseed)
                    python -m seed.seed --flood path/to/real.geojson --source "Bhuvan/NDEM ..."

All reports created here have synthetic=true and "SYNTHETIC" printed on the photo.
"""

import argparse
import io
import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw
from sqlalchemy import delete, func, select

from app.auth import hash_password
from app.config import get_settings
from app.db import SessionLocal, init_db
from app.models import (
    Asset,
    FloodLayer,
    Grievance,
    Photo,
    Report,
    StatusHistory,
    User,
    utcnow,
)
from app.services.phash import phash_bytes
from app.services.photostore import DbPhotoStore
from app.services.verify import run_checks

HERE = Path(__file__).parent
DEMO_PASSWORD = "meetpu123"

# (district, taluk, village, lat, lon). First block sits inside the demo flood layer, second outside.
PLACES_IN = [
    ("Chennai", "Velachery", "Velachery", 12.978, 80.218),
    ("Chennai", "Sholinganallur", "Pallikaranai", 12.948, 80.214),
    ("Chennai", "Velachery", "Madipakkam", 12.964, 80.203),
    ("Chengalpattu", "Tambaram", "Mudichur", 12.916, 80.072),
    ("Kancheepuram", "Kundrathur", "Varadharajapuram", 12.921, 80.093),
    ("Chennai", "Tiruvottiyur", "Manali", 13.172, 80.270),
    ("Chennai", "Tiruvottiyur", "Ennore", 13.188, 80.292),
]
PLACES_OUT = [
    ("Chennai", "Aminjikarai", "Anna Nagar", 13.085, 80.210),
    ("Chennai", "Maduravoyal", "Porur", 13.035, 80.157),
    ("Chengalpattu", "Vandalur", "Guduvanchery", 12.845, 80.060),
]

CITIZEN_NAMES = [
    "Murugan K", "Lakshmi R", "Selvam P", "Kavitha S", "Arumugam V", "Meena D", "Rajesh T",
    "Saranya M", "Palani A", "Revathi G", "Karthik N", "Deepa J", "Senthil B", "Anitha L",
    "Ganesan R", "Priya K", "Velu S", "Malar P", "Kumar V", "Jothi M",
]
DAMAGE_BY_ASSET = {
    "house": ["partially_damaged", "fully_damaged", "submerged"],
    "hut": ["fully_damaged", "washed_away", "partially_damaged"],
    "cattle": ["dead"],
    "crop": ["submerged"],
    "boat": ["washed_away", "partially_damaged"],
    "shop": ["submerged", "partially_damaged"],
}
ASSET_WEIGHTS = {"house": 6, "hut": 5, "cattle": 2, "crop": 2, "boat": 1, "shop": 2}

# Status mix for 50 reports
STATUS_PLAN = ["reported"] * 20 + ["verified"] * 12 + ["rejected"] * 4 + ["approved"] * 9 + ["paid"] * 5


def synthetic_photo(rng: random.Random, label: str) -> bytes:
    img = Image.new("RGB", (640, 480), tuple(rng.randint(40, 200) for _ in range(3)))
    draw = ImageDraw.Draw(img)
    for _ in range(rng.randint(6, 12)):
        x0, y0 = rng.randint(0, 600), rng.randint(0, 440)
        x1, y1 = x0 + rng.randint(40, 300), y0 + rng.randint(40, 250)
        color = tuple(rng.randint(0, 255) for _ in range(3))
        if rng.random() < 0.5:
            draw.rectangle([x0, y0, x1, y1], fill=color)
        else:
            draw.ellipse([x0, y0, x1, y1], fill=color)
    draw.rectangle([0, 430, 640, 480], fill=(0, 0, 0))
    draw.text((12, 445), f"SYNTHETIC DEMO PHOTO - {label}", fill=(255, 255, 0))
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=85)
    return out.getvalue()


def load_flood(db, path: Path, event: str, source: str | None, start: datetime, end: datetime) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    source = source or data.get("properties", {}).get("source") or path.name
    db.execute(delete(FloodLayer).where(FloodLayer.event_name == event))
    count = 0
    for i, feat in enumerate(data["features"]):
        geom = feat.get("geometry")
        if not geom or geom["type"] not in ("Polygon", "MultiPolygon"):
            continue
        db.add(FloodLayer(
            event_name=event,
            name=(feat.get("properties") or {}).get("name") or f"polygon {i + 1}",
            geom=func.ST_Multi(func.ST_MakeValid(func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(geom)), 4326))),
            source=source[:200],
            event_start=start,
            event_end=end,
        ))
        count += 1
    return count


def upsert_user(db, **fields) -> User:
    key = {"phone": fields["phone"]} if fields.get("phone") else {"username": fields["username"]}
    user = db.scalar(select(User).filter_by(**key))
    if user is None:
        user = User(**fields)
        db.add(user)
    else:
        for k, v in fields.items():
            setattr(user, k, v)
    db.flush()
    return user


def seed_users(db) -> dict:
    pw = hash_password(DEMO_PASSWORD)
    users = {
        "staff_chennai": upsert_user(db, phone="9800000001", role="staff", name="VAO Ramesh (Chennai)",
                                     district="Chennai", taluk="Velachery"),
        "staff_chengalpattu": upsert_user(db, phone="9800000002", role="staff", name="VAO Sumathi (Chengalpattu)",
                                          district="Chengalpattu", taluk="Tambaram"),
        "official": upsert_user(db, username="collector", password_hash=pw, role="official",
                                name="District Collector Office (demo)", district="Chennai"),
        "admin": upsert_user(db, username="admin", password_hash=pw, role="admin", name="Meetpu Admin"),
        "citizen_demo": upsert_user(db, phone="9000000000", role="citizen", name="Demo Citizen"),
    }
    users["citizens"] = [
        upsert_user(db, phone=f"90000000{i + 1:02d}", role="citizen", name=name)
        for i, name in enumerate(CITIZEN_NAMES)
    ]
    return users


def wipe_synthetic(db) -> None:
    ids = select(Report.id).where(Report.synthetic.is_(True))
    asset_ids = select(Report.asset_id).where(Report.synthetic.is_(True))
    for model in (StatusHistory, Grievance, Photo):
        db.execute(delete(model).where(model.report_id.in_(ids)))
    asset_list = list(db.scalars(asset_ids))
    db.execute(delete(Report).where(Report.synthetic.is_(True)))
    if asset_list:
        db.execute(delete(Asset).where(Asset.id.in_(asset_list)))


def seed_reports(db, users: dict, rng: random.Random, n: int = 50) -> None:
    now = utcnow()
    staff_for = {"Chennai": users["staff_chennai"]}
    plan = STATUS_PLAN[:n] + ["reported"] * max(0, n - len(STATUS_PLAN))
    rng.shuffle(plan)

    # Indexes for special cases
    dup_idx = {5: 1, 17: 9, 33: 21}           # report i reuses the photo of report j
    mismatch_idx = {3, 14, 27}               # EXIF GPS about 1.1 km off
    no_exif_idx = {8, 19, 30, 41, 46}
    photos: dict[int, bytes] = {}

    for i in range(n):
        inside = rng.random() < 0.78
        district, taluk, village, lat, lon = rng.choice(PLACES_IN if inside else PLACES_OUT)
        lat += rng.uniform(-0.002, 0.002)
        lon += rng.uniform(-0.002, 0.002)
        asset_type = rng.choices(list(ASSET_WEIGHTS), weights=list(ASSET_WEIGHTS.values()))[0]
        citizen = rng.choice(users["citizens"])
        status = plan[i]

        created = now - timedelta(hours=rng.uniform(6, 12 * 24))
        captured = created - timedelta(minutes=rng.randint(2, 90))

        asset = Asset(owner_user_id=citizen.id, type=asset_type, lat=lat, lon=lon,
                      geom=func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326), village=village)
        db.add(asset)
        db.flush()

        report = Report(
            id=uuid.uuid4(), asset_id=asset.id, reporter_id=citizen.id,
            damage_type=rng.choice(DAMAGE_BY_ASSET[asset_type]),
            severity_hint=rng.randint(1, 5),
            description=f"Synthetic demo report: {asset_type} damage in {village}.",
            lat=lat, lon=lon, geom=func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326),
            district=district, taluk=taluk, village=village,
            captured_at=captured, status="reported", status_changed_at=created,
            synthetic=True, created_at=created, flags=[],
        )
        db.add(report)
        db.flush()

        raw = photos[dup_idx[i]] if i in dup_idx and dup_idx[i] in photos else synthetic_photo(rng, village)
        photos[i] = raw
        report.photo_phash = phash_bytes(raw)
        report.photo_id = DbPhotoStore(db).put(report.id, raw)
        if i not in no_exif_idx:
            off = 0.01 if i in mismatch_idx else rng.uniform(-0.0003, 0.0003)
            report.exif_lat, report.exif_lon = lat + off, lon + off
            report.exif_taken_at = captured
        run_checks(db, report)

        # Walk the status history forward with backdated timestamps.
        history = [("reported", None, citizen, "Report submitted", created)]
        t = created
        staff = staff_for.get(district, users["staff_chengalpattu"])
        steps = {
            "verified": ["verified"],
            "rejected": ["rejected"],
            "approved": ["verified", "approved"],
            "paid": ["verified", "approved", "paid"],
        }.get(status, [])
        if status == "rejected" and rng.random() < 0.5:
            steps = ["verified", "rejected"]
        for step in steps:
            t = min(now - timedelta(minutes=5), t + timedelta(hours=rng.uniform(4, 70)))
            actor = staff if step in ("verified",) or (step == "rejected" and len(steps) == 1) else users["official"]
            note = {
                "verified": "Site visited, damage matches photo",
                "rejected": "Damage not found at site" if len(steps) == 1 else "Duplicate of earlier claim",
                "approved": "Approved under SDRF norms",
                "paid": "Mock payment",
            }[step]
            history.append((step, history[-1][0], actor, note, t))
        prev = None
        for to_s, _, actor, note, at in history:
            db.add(StatusHistory(report_id=report.id, from_status=prev, to_status=to_s,
                                 actor_id=actor.id, note=note, created_at=at))
            prev = to_s
        report.status = history[-1][0]
        report.status_changed_at = history[-1][4]
        if report.status == "paid":
            report.payment_ref = f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}"
        if report.status == "rejected" and rng.random() < 0.6:
            db.add(Grievance(report_id=report.id, user_id=citizen.id,
                             text="My house was damaged. Please visit again.", created_at=t))
    db.flush()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reset", action="store_true", help="delete synthetic reports before seeding")
    ap.add_argument("--flood", type=Path, default=HERE / "flood.geojson", help="flood extent GeoJSON")
    ap.add_argument("--source", help="source label for the flood layer")
    ap.add_argument("--event", default=get_settings().active_event)
    ap.add_argument("--window-days", type=int, default=14,
                    help="event window = now +/- this many days, so live demo reports pass the time check")
    ap.add_argument("--count", type=int, default=50)
    ap.add_argument("--seed", type=int, default=2023)
    args = ap.parse_args()

    init_db()
    now = utcnow()
    with SessionLocal() as db:
        n_poly = load_flood(db, args.flood, args.event, args.source,
                            now - timedelta(days=args.window_days), now + timedelta(days=args.window_days))
        users = seed_users(db)
        if args.reset:
            wipe_synthetic(db)
        existing = db.scalar(select(func.count()).select_from(Report).where(Report.synthetic.is_(True)))
        if existing:
            print(f"{existing} synthetic reports already present; use --reset to reseed.")
        else:
            seed_reports(db, users, random.Random(args.seed), args.count)
        # Re-run checks on real reports too, since the flood layer may have changed.
        for report in db.scalars(select(Report).where(Report.synthetic.is_(False))).unique():
            run_checks(db, report)
        db.commit()
        total = db.scalar(select(func.count()).select_from(Report))
    print(f"Flood layer '{args.event}': {n_poly} polygons. Reports in DB: {total}.")
    print(f"Portal login: collector / {DEMO_PASSWORD}   (admin / {DEMO_PASSWORD})")
    print(f"Staff OTP login: 9800000001 or 9800000002, code {get_settings().mock_otp_code}")
    print(f"Citizen OTP login: 9000000000, code {get_settings().mock_otp_code}")


if __name__ == "__main__":
    main()
