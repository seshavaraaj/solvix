"""Read GPS and capture time from the ORIGINAL photo bytes, before any resize strips EXIF."""

import io
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from PIL import Image

_GPS_IFD = 0x8825
_EXIF_IFD = 0x8769
_DATETIME_ORIGINAL = 0x9003
_DATETIME = 0x0132

# IST, since phone EXIF times carry no zone and the demo region is Tamil Nadu.
_IST = timedelta(hours=5, minutes=30)


@dataclass
class ExifInfo:
    lat: float | None = None
    lon: float | None = None
    taken_at: datetime | None = None

    @property
    def has_gps(self) -> bool:
        return self.lat is not None and self.lon is not None


def _to_deg(value) -> float:
    d, m, s = (float(v) for v in value)
    return d + m / 60 + s / 3600


def read_exif(raw: bytes) -> ExifInfo:
    info = ExifInfo()
    try:
        exif = Image.open(io.BytesIO(raw)).getexif()
    except Exception:
        return info

    try:
        gps = exif.get_ifd(_GPS_IFD)
        if gps and 2 in gps and 4 in gps:
            lat = _to_deg(gps[2])
            lon = _to_deg(gps[4])
            if gps.get(1) == "S":
                lat = -lat
            if gps.get(3) == "W":
                lon = -lon
            if not (lat == 0 and lon == 0):
                info.lat, info.lon = lat, lon
    except Exception:
        pass

    try:
        stamp = exif.get_ifd(_EXIF_IFD).get(_DATETIME_ORIGINAL) or exif.get(_DATETIME)
        if stamp:
            local = datetime.strptime(str(stamp).strip("\x00 "), "%Y:%m:%d %H:%M:%S")
            info.taken_at = local.replace(tzinfo=timezone.utc) - _IST
    except Exception:
        pass
    return info


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
