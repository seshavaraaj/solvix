"""Perceptual hash (pHash) in pure Python, so the backend needs no numpy/scipy.

Algorithm: grayscale 32x32, 2D DCT-II, keep the top-left 8x8 low frequencies,
set each bit by comparing to the median (DC term excluded from the median).
Result: 64-bit hash as 16 hex chars. Similar images differ by few bits.
"""

import io
import math

from PIL import Image

_N = 32
_K = 8
_COS = [[math.cos(math.pi * u * (2 * x + 1) / (2 * _N)) for x in range(_N)] for u in range(_K)]


def _dct_low(pixels: list[list[float]]) -> list[list[float]]:
    # Separable DCT, computing only the first _K coefficients per axis.
    rows = [[sum(row[x] * _COS[u][x] for x in range(_N)) for u in range(_K)] for row in pixels]
    return [[sum(rows[y][u] * _COS[v][y] for y in range(_N)) for u in range(_K)] for v in range(_K)]


def phash_image(img: Image.Image) -> str:
    gray = img.convert("L").resize((_N, _N), Image.Resampling.LANCZOS)
    data = gray.tobytes()
    pixels = [[float(data[y * _N + x]) for x in range(_N)] for y in range(_N)]
    coeffs = [c for row in _dct_low(pixels) for c in row]
    median = sorted(coeffs[1:])[len(coeffs[1:]) // 2]
    bits = 0
    for c in coeffs:
        bits = (bits << 1) | (1 if c > median else 0)
    return f"{bits:016x}"


def phash_bytes(raw: bytes) -> str:
    return phash_image(Image.open(io.BytesIO(raw)))


def hamming(a: str, b: str) -> int:
    return (int(a, 16) ^ int(b, 16)).bit_count()
