from __future__ import annotations

from datetime import datetime, timezone
from email.utils import format_datetime, parsedate_to_datetime
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path, PurePath
from typing import Any, Optional, Sequence, SupportsFloat, Type
from uuid import UUID

from .types import DecodeError, Decoder, DParser, DStep, EncodeError, Encoder, EParser


def _base_encoder(t: Type) -> Encoder:
    def e(
        tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]
    ) -> Optional[EParser]:

        if issubclass(tp, t):

            def p(x: Any) -> DStep:
                if isinstance(x, t):
                    return True, str(x)
                else:
                    return False, EncodeError(path=(*path, tp), actual=x)

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


"""
UNIX
"""


def unix_date_encoder(
    tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]
) -> Optional[EParser]:
    if issubclass(tp, datetime):

        def p(x: Any) -> DStep:
            if isinstance(x, datetime):
                return True, x.replace(tzinfo=timezone.utc).timestamp()
            else:
                return False, EncodeError(path=(*path, tp), actual=x)

        return p
    else:
        return None


def unix_date_decoder(
    tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
) -> Optional[DParser]:
    if not issubclass(tp, datetime):
        return None
    else:

        def cont(x: Any) -> DStep:
            if not isinstance(x, SupportsFloat):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                try:
                    return True, datetime.fromtimestamp(x, tz=timezone.utc)
                except ValueError as e:
                    return False, DecodeError(e, path=(*path, tp), actual=x)

        return cont


"""
ISO Date
"""


def iso_date_encoder(
    tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]
) -> Optional[EParser]:
    if issubclass(tp, datetime):

        def p(x: Any) -> DStep:
            if isinstance(x, datetime):
                return True, x.replace(tzinfo=timezone.utc).isoformat()
            else:
                return False, EncodeError(path=(*path, tp), actual=x)

        return p
    else:
        return None


def iso_date_decoder(
    tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
) -> Optional[DParser]:
    if not issubclass(tp, datetime):
        return None
    else:

        def cont(x: Any) -> DStep:
            if not isinstance(x, str):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                try:
                    return True, datetime.fromisoformat(x).replace(tzinfo=timezone.utc)
                except ValueError as e:
                    return False, DecodeError(e, path=(*path, tp), actual=x)

        return cont


"""
Internet Date
"""


def internet_date_encoder(
    tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]
) -> Optional[EParser]:
    if issubclass(tp, datetime):

        def p(x: Any) -> DStep:
            if isinstance(x, datetime):
                return True, format_datetime(
                    x.replace(tzinfo=timezone.utc), usegmt=True
                )
            else:
                return False, EncodeError(path=(*path, tp), actual=x)

        return p
    else:
        return None


def internet_date_decoder(
    tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
) -> Optional[DParser]:
    if not issubclass(tp, datetime):
        return None
    else:

        def cont(x: Any) -> DStep:
            if not isinstance(x, str):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                try:
                    return True, parsedate_to_datetime(x).replace(tzinfo=timezone.utc)
                except ValueError as e:
                    return False, DecodeError(e, path=(*path, tp), actual=x)

        return cont
