from __future__ import annotations

from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path, PurePath
from typing import Any, Optional, Sequence, Type
from uuid import UUID

from .types import DecodeError, Decoder, DParser, DStep, Encoder, EParser


def _base_encoder(t: Type) -> Encoder:
    def e(
        tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]
    ) -> Optional[EParser]:

        if issubclass(tp, t):

            def p(x: Any) -> DStep:
                if isinstance(x, t):
                    try:
                        return True, str(x)
                    except ValueError as e:
                        return False, DecodeError(e, path=(*path, tp), actual=x)
                else:
                    return False, DecodeError(path=(*path, tp), actual=x)

            return p
        else:
            return None

    return e


DEFAULT_ENCODERS = (
    _base_encoder(UUID),
    _base_encoder(PurePath),
    _base_encoder(IPv6Network),
    _base_encoder(IPv4Network),
    _base_encoder(IPv6Address),
    _base_encoder(IPv4Address),
)


def _base_decoder(t: Type) -> Decoder:
    def d(
        tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
    ) -> Optional[DParser]:

        if issubclass(tp, t):

            def p(x: Any) -> DStep:
                if isinstance(x, str):
                    try:
                        return True, t(x)
                    except ValueError as e:
                        return False, DecodeError(e, path=(*path, tp), actual=x)
                else:
                    return False, DecodeError(path=(*path, tp), actual=x)

            return p
        else:
            return None

    return d


DEFAULT_DECODERS = (
    _base_decoder(UUID),
    _base_decoder(Path),
    _base_decoder(PurePath),
    _base_decoder(IPv6Network),
    _base_decoder(IPv4Network),
    _base_decoder(IPv6Interface),
    _base_decoder(IPv4Interface),
    _base_decoder(IPv6Address),
    _base_decoder(IPv4Address),
)

