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


class _BaseDecoder(Decoder):
    def __init__(self, t: Type) -> None:
        self._t = t

    def __call__(
        self, tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
    ) -> Optional[DParser]:
        if isinstance(tp, self._t):

            def parser(x: Any) -> DStep:
                try:
                    return True, self._t(x)
                except ValueError as e:
                    return False, DecodeError(e, path=(*path, tp), actual=x)

            return parser
        else:
            return None


DEFAULT_DECODERS = (
    _BaseDecoder(UUID),
    _BaseDecoder(Path),
    _BaseDecoder(PurePath),
    _BaseDecoder(IPv6Network),
    _BaseDecoder(IPv4Network),
    _BaseDecoder(IPv6Interface),
    _BaseDecoder(IPv4Interface),
    _BaseDecoder(IPv6Address),
    _BaseDecoder(IPv4Address),
)

