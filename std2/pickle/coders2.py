from typing import Any
from uuid import UUID

from .types import DStep, DecodeError, DParser


def _is_uuid(x: Any) -> bool:
    return isinstance(x, UUID)


def _uuid_encode(x: UUID) -> str:
    return str(x)


def _uuid_decode(x: Any) -> DStep:
    try:
        return True, UUID(x)
    except ValueError:
        return False, ""

