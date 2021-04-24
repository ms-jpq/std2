from datetime import datetime, timezone
from inspect import isclass
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
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


"""
ipaddr -> str
"""


def ipv4_addr_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, IPv4Address):
        raise EncodeError()
    else:
        return str(thing)


def ipv6_addr_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, IPv6Address):
        raise EncodeError()
    else:
        return str(thing)


def ipv4_addr_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> IPv4Address:
    if not (isclass(tp) and issubclass(tp, IPv4Address) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return IPv4Address(thing)


def ipv6_addr_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> IPv6Address:
    if not (isclass(tp) and issubclass(tp, IPv6Address) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return IPv6Address(thing)


"""
ipnetwork -> str
"""


def ipv4_network_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, IPv4Network):
        raise EncodeError()
    else:
        return str(thing)


def ipv6_network_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, IPv6Network):
        raise EncodeError()
    else:
        return str(thing)


def ipv4_network_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> IPv4Network:
    if not (isclass(tp) and issubclass(tp, IPv4Network) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return IPv4Network(thing)


def ipv6_network_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> IPv6Network:
    if not (isclass(tp) and issubclass(tp, IPv6Network) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return IPv6Network(thing)


"""
ipinterface -> str
"""


def ipv4_interface_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, IPv4Interface):
        raise EncodeError()
    else:
        return str(thing)


def ipv6_interface_encoder(thing: Any, encoders: Encoders) -> str:
    if not isinstance(thing, IPv6Interface):
        raise EncodeError()
    else:
        return str(thing)


def ipv4_interface_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> IPv4Interface:
    if not (isclass(tp) and issubclass(tp, IPv4Interface) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return IPv4Interface(thing)


def ipv6_interface_decoder(
    tp: Any, thing: Any, strict: bool, decoders: Decoders, path: Sequence[Any]
) -> IPv6Interface:
    if not (isclass(tp) and issubclass(tp, IPv6Interface) and isinstance(thing, str)):
        raise DecodeError(path=(*path, tp), actual=thing)
    else:
        return IPv6Interface(thing)


"""
Builtins
"""

BUILTIN_ENCODERS: Encoders = (
    path_encoder,
    uuid_encoder,
    datetime_str_encoder,
    ipv4_addr_encoder,
    ipv6_addr_encoder,
    ipv4_network_encoder,
    ipv6_network_encoder,
    ipv4_interface_encoder,
    ipv6_interface_encoder,
)

BUILTIN_DECODERS: Decoders = (
    path_decoder,
    uuid_decoder,
    datetime_str_decoder,
    ipv4_addr_decoder,
    ipv6_addr_decoder,
    ipv4_network_decoder,
    ipv6_network_decoder,
    ipv4_interface_decoder,
    ipv6_interface_decoder,
)
