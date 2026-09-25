"""End-to-end lifecycle check against a running API.

Usage (from backend/):  python -m scripts.smoke                      (http://localhost:8000)
                        python -m scripts.smoke https://meetpu-api.onrender.com

Needs the seed to have run (staff and collector accounts, flood layer).
"""

import io
import sys
import uuid
from datetime import datetime, timezone

import httpx
from PIL import Image, ImageDraw

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000").rstrip("/")
OTP = "123456"
INSIDE = (12.978, 80.218)   # Velachery, inside demo flood layer
OUTSIDE = (13.085, 80.210)  # Anna Nagar, outside


def photo_with_gps(lat: float, lon: float, seed: int) -> bytes:
    img = Image.new("RGB", (640, 480), (30 + seed * 40 % 200, 90, 140))
    ImageDraw.Draw(img).ellipse([100 + seed * 20, 80, 400, 380], fill=(200, 180 - seed * 30 % 150, 40))
    exif = Image.Exif()
    gps = exif.get_ifd(0x8825)

    def dms(v: float):
        d = int(v)
        m = int((v - d) * 60)
        return (float(d), float(m), round(((v - d) * 60 - m) * 60, 2))

    gps[1], gps[2], gps[3], gps[4] = "N", dms(lat), "E", dms(lon)
    exif.get_ifd(0x8769)[0x9003] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", exif=exif)
    return buf.getvalue()


def otp_login(c: httpx.Client, phone: str) -> dict:
    c.post("/auth/otp", json={"phone": phone}).raise_for_status()
    r = c.post("/auth/verify", json={"phone": phone, "code": OTP, "name": "Smoke Test"})
    r.raise_for_status()
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def check(label: str, cond: bool, detail=""):
    print(("PASS " if cond else "FAIL ") + label + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        sys.exit(1)


def main():
    with httpx.Client(base_url=BASE, timeout=60) as c:
        check("health", c.get("/health").json().get("ok") is True)

        citizen = otp_login(c, "9111111111")
        staff = otp_login(c, "9800000001")
        r = c.post("/auth/login", json={"username": "collector", "password": "meetpu123"})
        check("official login", r.status_code == 200, r.text)
        official = {"Authorization": f"Bearer {r.json()['access_token']}"}

        rid = str(uuid.uuid4())
        body = {
            "id": rid, "asset_type": "house", "damage_type": "partially_damaged", "severity_hint": 3,
            "lat": INSIDE[0], "lon": INSIDE[1], "captured_at": datetime.now(timezone.utc).isoformat(),
            "district": "Chennai", "taluk": "Velachery", "village": "Velachery",
        }
        r = c.post("/reports", json=body, headers=citizen)
        check("create report", r.status_code == 201, r.text)
        check("inside flood extent", r.json()["in_flood_extent"] is True, r.json())

        r = c.post("/reports", json=body, headers=citizen)
        check("retry is idempotent (200, same id)", r.status_code == 200 and r.json()["id"] == rid, r.text)

        raw = photo_with_gps(*INSIDE, seed=uuid.UUID(rid).int % 7)
        r = c.post(f"/reports/{rid}/photo", files={"file": ("p.jpg", raw, "image/jpeg")}, headers=citizen)
        check("photo upload", r.status_code == 200, r.text)
        codes = {f["code"] for f in r.json()["flags"]}
        check("no gps_mismatch for matching EXIF", "gps_mismatch" not in codes, codes)
        check("photo served", c.get(r.json()["photo_url"]).status_code == 200)

        # Second report outside the flood area, reusing the same photo
        rid2 = str(uuid.uuid4())
        r = c.post("/reports", json={**body, "id": rid2, "lat": OUTSIDE[0], "lon": OUTSIDE[1]}, headers=citizen)
        check("outside flood extent flagged", r.json()["in_flood_extent"] is False, r.json())
        r = c.post(f"/reports/{rid2}/photo", files={"file": ("p.jpg", raw, "image/jpeg")}, headers=citizen)
        codes = {f["code"] for f in r.json()["flags"]}
        check("duplicate photo flagged", "duplicate_photo" in codes, codes)
        check("gps mismatch flagged", "gps_mismatch" in codes, codes)

        r = c.post(f"/reports/{rid}/approve", json={}, headers=official)
        check("cannot approve before verify (409)", r.status_code == 409, r.text)
        r = c.post(f"/reports/{rid}/verify", json={"decision": "verified", "note": "Smoke"}, headers=citizen)
        check("citizen cannot verify (403)", r.status_code == 403, r.text)

        r = c.get("/reports?status=reported", headers=staff)
        check("staff queue lists report", any(x["id"] == rid for x in r.json()))

        check("verify", c.post(f"/reports/{rid}/verify", json={"decision": "verified", "note": "Site visit ok"},
                               headers=staff).status_code == 200)
        check("approve", c.post(f"/reports/{rid}/approve", json={"note": "SDRF"}, headers=official).status_code == 200)
        r = c.post(f"/reports/{rid}/pay", json={"amount_inr": 5000}, headers=official)
        check("mock pay", r.status_code == 200 and r.json()["payment_ref"].startswith("MOCKPAY"), r.text)

        mine = {x["id"]: x for x in c.get("/me/reports", headers=citizen).json()}
        steps = [h["to_status"] for h in mine[rid]["history"]]
        check("citizen timeline", steps == ["reported", "verified", "approved", "paid"], steps)
        check("history has actor", all(h["actor_id"] for h in mine[rid]["history"]))

        r = c.post(f"/reports/{rid2}/grievance", json={"text": "Please recheck"}, headers=citizen)
        check("grievance", r.status_code == 201, r.text)

        r = c.get("/dashboard/stuck", headers=official)
        check("stuck dashboard", r.status_code == 200 and "by_status" in r.json(), r.text)
        r = c.get("/export/pdna", headers=official)
        check("pdna export includes paid case", r.status_code == 200 and rid in r.text, r.status_code)
        check("flood layer geojson", c.get("/flood-layer/michaung-2023").json()["type"] == "FeatureCollection")
    print("All smoke checks passed.")


if __name__ == "__main__":
    main()
