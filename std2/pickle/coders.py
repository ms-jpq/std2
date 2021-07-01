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

from .types import DecodeError, Decoder, DParser, DStep


def _base_decoder(t: Type) -> Decoder:
    def d(
        tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
    ) -> Optional[DParser]:

        if isinstance(tp, t):

            def parser(x: Any) -> DStep:
                try:
                    return True, t(x)
                except ValueError as e:
                    return False, DecodeError(e, path=(*path, tp), actual=x)

            return parser
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


