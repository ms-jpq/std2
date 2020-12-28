from collections.abc import (
    ByteString,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Set,
)
from dataclasses import fields, is_dataclass
from enum import Enum
from inspect import isclass
from itertools import chain, repeat
from operator import attrgetter
from typing import Any, Callable, Dict, FrozenSet, Iterator, List
from typing import Mapping as T_Mapping
from typing import MutableMapping as T_MutableMapping
from typing import MutableSequence as T_MutableSequence
from typing import MutableSet as T_MutableSet
from typing import Optional
from typing import Sequence as T_Sequence
from typing import Set as T_Set
from typing import TypeVar, Union, cast, get_args, get_origin

T = TypeVar("T")


_MAPS_M = {MutableMapping, T_MutableMapping, Dict, dict}
_MAPS = {Mapping, T_Mapping} | _MAPS_M

_SETS_M = {MutableSet, T_MutableSet, Set, T_Set, set}
_SETS = {FrozenSet, frozenset} | _SETS_M

_SEQS_M = {MutableSequence, T_MutableSequence, List, list}
_SEQS = {Sequence, T_Sequence} | _SEQS_M


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


def decode(tp: Any, thing: Any, parent: Optional[Any] = None) -> T:
    origin, args = get_origin(tp), get_args(tp)

    if tp is Any:
        return cast(T, thing)

    elif tp is None:
        if thing is not None:
            raise DecodeError(parent, tp, thing)
        else:
            return cast(T, thing)

    elif origin is Union:
        errs: MutableSequence[Exception] = []
        for member in args:
            try:
                return decode(member, thing, parent=tp)
            except DecodeError as e:
                errs.append(e)
        else:
            raise DecodeError(parent, tp, thing, errs)

    elif origin in _MAPS:
        if not isinstance(thing, Mapping):
            raise DecodeError(parent, tp, thing)
        else:
            lhs, rhs = args
            mapping: Mapping[Any, Any] = {
                decode(lhs, k, parent=tp): decode(rhs, v, parent=tp)
                for k, v in thing.items()
            }
            return cast(T, mapping)

    elif origin in _SETS:
        if not isinstance(thing, Iterable):
            raise DecodeError(parent, tp, thing)
        else:
            t, *_ = args
            it: Iterator[Any] = (decode(t, item, parent=tp) for item in thing)
            return cast(T, {*it} if origin in _SETS_M else frozenset(it))

    elif origin in _SEQS:
        if not isinstance(thing, Iterable):
            raise DecodeError(parent, tp, thing)
        else:
            t, *_ = args
            it = (decode(t, item, parent=tp) for item in thing)
            return cast(T, [*it] if origin in _SEQS_M else tuple(it))

    elif origin is tuple:
        if not isinstance(thing, Sequence):
            raise DecodeError(parent, tp, thing)
        else:
            tps = (
                chain(args[:-1], repeat(args[-2]))
                if len(args) >= 2 and args[-1] is Ellipsis
                else args
            )
            return cast(
                T, tuple(decode(t, item, parent=tp) for t, item in zip(tps, thing))
            )

    elif isclass(tp) and issubclass(tp, Enum):
        return cast(T, tp(thing))

    elif is_dataclass(tp):
        if not isinstance(thing, Mapping):
            raise DecodeError(parent, tp, thing)
        else:
            kwargs: Mapping[str, Any] = {
                field.name: decode(field.type, thing[field.name], parent=tp)
                for field in fields(tp)
                if field.name in thing
            }
            try:
                return cast(Callable[..., T], tp)(**kwargs)
            except TypeError as e:
                raise DecodeError(parent, tp, thing, e)

    else:
        if not isinstance(thing, tp):
            raise DecodeError(parent, tp, thing)
        else:
            return cast(T, thing)
