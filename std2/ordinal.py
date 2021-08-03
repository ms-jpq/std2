from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, TypeVar


class _SupportsLT(Protocol):
    @abstractmethod
    def __lt__(self, other: _SupportsLT) -> bool:
        ...


SupportsLT = TypeVar("SupportsLT", bound=_SupportsLT)


def clamp(lo: SupportsLT, n: SupportsLT, hi: SupportsLT) -> SupportsLT:
    return max(lo, min(hi, n))
