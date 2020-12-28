from collections.abc import ByteString, Iterable, Mapping, Sequence, Set
from dataclasses import fields, is_dataclass
from enum import Enum
from itertools import chain, repeat
from operator import attrgetter
from typing import Any, Callable, TypeVar, Union, cast, get_args, get_origin

T = TypeVar("T")


class DecodeError(Exception):
    ...


def encode(thing: Any) -> Any:
    if isinstance(thing, Mapping):
        return {encode(k): encode(v) for k, v in thing.items()}

    elif isinstance(thing, Iterable) and not isinstance(thing, (str, ByteString)):
        return tuple(thing)

    elif isinstance(thing, Enum):
        return thing.value

    elif is_dataclass(thing):
        return {
            field.name: encode(attrgetter(field.name)(thing)) for field in fields(thing)
        }

    else:
        return thing


def decode(tp: Any, thing: Any) -> T:
    origin, args = get_origin(tp), get_args(tp)

    if tp is Any:
        return thing

    elif tp is None:
        if thing is not None:
            raise DecodeError(tp, thing)
        else:
            return cast(T, thing)

    elif origin is Union:
        for member in args:
            try:
                return decode(member, thing)
            except DecodeError:
                pass
        else:
            raise DecodeError(tp, thing)

    elif origin in {Mapping, dict}:
        if not isinstance(thing, Mapping):
            raise DecodeError(tp, thing)
        else:
            lhs, rhs = args
            return cast(T, {decode(lhs, k): decode(rhs, v) for k, v in thing.items()})

    elif origin is Set:
        if not isinstance(thing, Iterable):
            raise DecodeError(tp, thing)
        else:
            t, *_ = args
            return cast(T, {decode(t, item) for item in thing})

    elif origin in {Sequence, list}:
        if not isinstance(thing, Iterable):
            raise DecodeError(tp, thing)
        else:
            t, *_ = args
            it = (decode(t, item) for item in thing)
            return cast(T, tuple(it) if origin is Sequence else [*it])

    elif origin is tuple:
        if not isinstance(thing, Sequence):
            raise DecodeError(tp, thing)
        else:
            tps = (
                chain(args[:-1], repeat(args[-2]))
                if len(args) >= 2 and args[-1] is Ellipsis
                else args
            )
            return cast(T, tuple(decode(t, item) for t, item in zip(tps, thing)))

    elif issubclass(tp, Enum):
        return cast(T, tp(thing))

    elif is_dataclass(tp):
        if not isinstance(thing, Mapping):
            raise DecodeError(tp, thing)
        else:
            return cast(Callable[..., T], tp)(
                **{
                    field.name: decode(field.type, thing[field.name])
                    for field in fields(tp)
                    if field.name in thing
                }
            )

    else:
        if not isinstance(thing, tp):
            raise DecodeError(tp, thing)
        else:
            return cast(T, thing)
