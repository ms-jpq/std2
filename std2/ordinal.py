from .types import SupportsLT


def clamp(lo: SupportsLT, n: SupportsLT, hi: SupportsLT) -> SupportsLT:
    return max(lo, min(hi, n))
