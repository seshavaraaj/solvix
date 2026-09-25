"""Unit tests for the rule engine and helpers. No database needed."""

import io
import random
from datetime import datetime, timedelta, timezone

from PIL import Image

from app.auth import check_password, hash_password
from app.services.exif import haversine_m, read_exif
from app.services.phash import hamming, phash_bytes
from app.services.verify import RuleInput, evaluate
from seed.seed import synthetic_photo

NOW = datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc)


def rule_input(**kw) -> RuleInput:
    base = dict(
        lat=12.978, lon=80.218, in_flood_extent=True, has_photo=True,
        exif_lat=12.978, exif_lon=80.218, taken_at=NOW,
        event_start=NOW - timedelta(days=7), event_end=NOW + timedelta(days=7),
        duplicate_of=None, gps_mismatch_m=200,
    )
    base.update(kw)
    return RuleInput(**base)


def codes(flags):
    return {f["code"] for f in flags}


def test_clean_report_scores_100():
    score, flags = evaluate(rule_input())
    assert score == 100 and flags == []


def test_outside_flood_extent():
    score, flags = evaluate(rule_input(in_flood_extent=False))
    assert codes(flags) == {"outside_flood_extent"} and score == 60


def test_gps_mismatch_over_200m():
    score, flags = evaluate(rule_input(exif_lat=12.978 + 0.01))
    assert "gps_mismatch" in codes(flags)
    assert flags[0]["distance_m"] > 1000


def test_gps_within_200m_passes():
    _, flags = evaluate(rule_input(exif_lat=12.978 + 0.001))
    assert flags == []


def test_missing_exif_is_small_penalty():
    score, flags = evaluate(rule_input(exif_lat=None, exif_lon=None))
    assert codes(flags) == {"no_exif_gps"} and score == 90


def test_duplicate_and_window_stack_and_clamp():
    score, flags = evaluate(rule_input(
        in_flood_extent=False, duplicate_of="abc", taken_at=NOW - timedelta(days=30),
        exif_lat=13.5,
    ))
    assert codes(flags) == {"outside_flood_extent", "duplicate_photo", "gps_mismatch", "outside_event_window"}
    assert score == 0


def test_no_photo():
    _, flags = evaluate(rule_input(has_photo=False))
    assert codes(flags) == {"no_photo"}


def test_phash_same_image_after_resize_matches():
    raw = synthetic_photo(random.Random(1), "A")
    img = Image.open(io.BytesIO(raw)).resize((320, 240))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=60)
    assert hamming(phash_bytes(raw), phash_bytes(buf.getvalue())) <= 6


def test_phash_different_images_differ():
    a = phash_bytes(synthetic_photo(random.Random(1), "A"))
    b = phash_bytes(synthetic_photo(random.Random(2), "B"))
    assert hamming(a, b) > 6


def test_exif_gps_roundtrip():
    img = Image.new("RGB", (64, 64), (100, 120, 140))
    exif = Image.Exif()
    gps = exif.get_ifd(0x8825)
    gps[1], gps[2] = "N", (12.0, 58.0, 40.8)
    gps[3], gps[4] = "E", (80.0, 13.0, 4.8)
    exif.get_ifd(0x8769)[0x9003] = "2026:09:25 15:30:00"
    buf = io.BytesIO()
    img.save(buf, format="JPEG", exif=exif)
    info = read_exif(buf.getvalue())
    assert info.has_gps
    assert abs(info.lat - 12.978) < 1e-4 and abs(info.lon - 80.218) < 1e-4
    assert info.taken_at == datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc)


def test_exif_missing():
    buf = io.BytesIO()
    Image.new("RGB", (8, 8)).save(buf, format="JPEG")
    assert not read_exif(buf.getvalue()).has_gps


def test_haversine():
    assert abs(haversine_m(13.0, 80.0, 13.01, 80.0) - 1112) < 5


def test_password_hash():
    h = hash_password("secret")
    assert check_password("secret", h) and not check_password("wrong", h)
