from typing import Tuple

_RGB_MIN = 0
_RGB_MAX = 255
_RGB_RANGE = range(_RGB_MIN, _RGB_MAX + 1)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    if r not in _RGB_RANGE or g not in _RGB_RANGE or b not in _RGB_RANGE:
        raise ValueError((r, g, b))
    else:
        _r, _g, _b = format(r, "02x"), format(g, "02x"), format(b, "02x")
        return f"#{_r}{_g}{_b}"


def rgb_inverse(r: int, g: int, b: int) -> Tuple[int, int, int]:
    if r not in _RGB_RANGE or g not in _RGB_RANGE or b not in _RGB_RANGE:
        raise ValueError((r, g, b))
    else:
        return _RGB_MAX - r, _RGB_MAX - g, _RGB_MAX - b


def hex_to_rgb(hex: str) -> Tuple[int, int, int]:
    prefix, r1, r2, g1, g2, b1, b2 = hex
    r, g, b = int(r1 + r2, 16), int(g1 + g2, 16), int(b1 + b2, 16)
    if (
        prefix != "#"
        or r not in _RGB_RANGE
        or g not in _RGB_RANGE
        or b not in _RGB_RANGE
    ):
        raise ValueError(hex)
    else:
        return r, g, b
