from inspect import isclass
from typing import Any, Optional
from uuid import UUID

from .decode import Decoders
from .encode import Encoders

_encode_is_uuid = lambda thing: isinstance(thing, UUID)


def _uuid_encoder(thing: UUID, encoders: Encoders) -> str:
    return thing.hex


_decode_is_uuid = lambda tp: isclass(tp) and issubclass(tp, UUID)


def _uuid_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, parent: Optional[Any]
) -> UUID:
    return UUID(hex=thing)


UUID_ENCODER: Encoders = {_encode_is_uuid: _uuid_encoder}
UUID_DECODER: Decoders = {_decode_is_uuid: _uuid_decoder}
