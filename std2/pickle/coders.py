from datetime import datetime, timezone
from inspect import isclass
from typing import Any, Sequence, SupportsFloat
from uuid import UUID

from .decode import DecodeError, Decoders
from .encode import EncodeError, Encoders


def uuid_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, UUID):
        raise EncodeError()
    else:
        return thing.hex


def uuid_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> UUID:
    if not (isclass(tp) and issubclass(tp, UUID) and isinstance(thing, str)):
        raise DecodeError(path=tuple((*path, tp)), actual=thing)
    else:
        return UUID(hex=thing)


def datetime_str_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, datetime):
        raise EncodeError()
    else:
        return thing.isoformat()


def datetime_str_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> datetime:
    if not (isclass(tp) and issubclass(tp, datetime) and isinstance(thing, str)):
        raise DecodeError(path=tuple((*path, tp)), actual=thing)
    else:
        return datetime.fromisoformat(thing)


def datetime_float_encoder(thing: Any, encoders: Encoders) -> float:
    if not isinstance(thing, datetime):
        raise EncodeError()
    else:
        return thing.timestamp()


def datetime_float_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> datetime:
    if not (
        isclass(tp) and issubclass(tp, datetime) and isinstance(thing, SupportsFloat)
    ):
        raise DecodeError(path=tuple((*path, tp)), actual=thing)
    else:
        return datetime.fromtimestamp(float(thing), tz=timezone.utc)
