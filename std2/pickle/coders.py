from datetime import datetime, timezone
from inspect import isclass
from pathlib import PurePath
from typing import Any, Sequence, SupportsFloat, cast
from uuid import UUID

from .decoder import DecodeError, Decoders
from .encoder import EncodeError, Encoders

"""
Pure Path -> str
"""


def path_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, PurePath):
        raise EncodeError()
    else:
        return str(thing)


def path_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> PurePath:
    if not (isclass(tp) and issubclass(tp, PurePath) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return cast(PurePath, tp(thing))


"""
UUID -> str
"""


def uuid_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, UUID):
        raise EncodeError()
    else:
        return thing.hex


def uuid_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> UUID:
    if not (isclass(tp) and issubclass(tp, UUID) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return UUID(hex=thing)


"""
datetime -> str
"""


def datetime_str_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, datetime):
        raise EncodeError()
    else:
        return thing.isoformat()


def datetime_str_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> datetime:
    if not (isclass(tp) and issubclass(tp, datetime) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return datetime.fromisoformat(thing)


"""
datetime -> float
"""


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
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return datetime.fromtimestamp(float(thing), tz=timezone.utc)
