from inspect import isclass
from typing import Any, Optional
from uuid import UUID

from .decode import DecodeError, Decoders
from .encode import EncodeError, Encoders


def uuid_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, UUID):
        raise EncodeError()
    else:
        return thing.hex


def uuid_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, parent: Optional[Any]
) -> UUID:
    if not isclass(tp) and issubclass(tp, UUID) and isinstance(thing, str):
        raise DecodeError()
    else:
        return UUID(hex=thing)
