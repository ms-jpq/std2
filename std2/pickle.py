from collections.abc import Mapping, Sequence, Set
from dataclasses import fields, is_dataclass
from typing import Any, Type, TypeVar, Union, get_args, get_origin

from .types import Void

T = TypeVar("T")


class CoderError(Exception):
    ...


def decode(tp: Type[T], thing: Any) -> T:
    origin, args = get_origin(tp), get_args(tp)
    if tp is None:
        if thing is not None:
            raise CoderError(tp, thing)
        else:
            return thing

    elif origin is Union:
        for member in args:
            try:
                return decode(member, thing)
            except CoderError:
                pass
        else:
            raise CoderError(tp, thing)

    elif origin is Mapping:
        if not isinstance(thing, Mapping):
            raise CoderError(tp, thing)
        else:
            lhs, rhs = args
            return {decode(lhs, k): decode(rhs, v) for k, v in thing.items()}

    elif origin is Set:
        if not isinstance(thing, Sequence):
            raise CoderError(tp, thing)
        else:
            t, *_ = args
            return {decode(t, item) for item in thing}

    elif origin is Sequence:
        if not isinstance(thing, Sequence):
            raise CoderError(tp, thing)
        else:
            t, *_ = args
            return tuple(decode(t, item) for item in thing)

    elif origin is tuple:
        Ellipsis

    elif is_dataclass(tp):
        if not isinstance(thing, Mapping):
            raise CoderError(tp, thing)
        else:
            f = fields(tp)
            for ff in f:
                ff.name
            return
    else:
        if not isinstance(thing, tp):
            raise CoderError(tp, thing)
        else:
            return thing
