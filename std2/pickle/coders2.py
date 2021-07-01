from typing import Any, Sequence
from uuid import UUID

from .types import DecodeError, Decoders, DStep


def _is_uuid(x: Any) -> bool:
    return isinstance(x, UUID)


def _uuid_encode(x: UUID) -> str:
    return str(x)


def _uuid_decode(
    x: Any, path: Sequence[Any], strict: bool, decoders: Decoders
) -> DStep:
    try:
        return True, UUID(x)
    except ValueError:
        return False, DecodeError(path=(*path, UUID), actual=x)

