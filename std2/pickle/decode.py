from __future__ import annotations

import builtins
from collections.abc import Iterable as ABC_Iterable
from collections.abc import Mapping as ABC_Mapping
from collections.abc import MutableMapping as ABC_MutableMapping
from collections.abc import MutableSequence as ABC_MutableSequence
from collections.abc import MutableSet as ABC_MutableSet
from collections.abc import Sequence as ABC_Sequence
from collections.abc import Set as ABC_Set
from dataclasses import fields, is_dataclass
from enum import Enum
from inspect import isclass
from itertools import chain, repeat
from operator import attrgetter
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Iterator,
    List,
    Literal,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    NoReturn,
    Protocol,
    Sequence,
    Set,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


_MAPS_M = {MutableMapping, ABC_MutableMapping, Dict, dict}
_MAPS = {Mapping, ABC_Mapping} | _MAPS_M

_SETS_M = {MutableSet, ABC_MutableSet, Set, ABC_Set, set}
_SETS = {FrozenSet, frozenset} | _SETS_M

_SEQS_M = {MutableSequence, ABC_MutableSequence, List, list}
_SEQS = {Sequence, ABC_Sequence} | _SEQS_M


class DecodeError(Exception):
    def __init__(
        self, *args: Any, parents: Sequence[Any], expected: Any, actual: Any
    ) -> None:
        super().__init__(parents, expected, actual, *args)
        self.parents, self.expected, self.actual = parents, expected, actual


class ExtraKeyError(DecodeError):
    def __init__(
        self,
        *args: Any,
        parents: Sequence[Any],
        expected: Any,
        actual: Any,
        keys: Sequence[Any]
    ) -> None:
        super().__init__(keys, *args, parents=parents, expected=expected, actual=actual)
        self.keys = keys


class Decoder(Protocol[T_co]):
    def __call__(
        self,
        tp: Any,
        thing: Any,
        strict: bool,
        decoders: Decoders,
        parents: Sequence[Any],
    ) -> T_co:
        ...


Decoders = Sequence[Decoder[Any]]


def decode(
    tp: Any,
    thing: Any,
    strict: bool = True,
    decoders: Decoders = (),
    parents: Sequence[Any] = (),
) -> T:
    new_parents = tuple((*parents, tp))

    def throw(*args: Any) -> NoReturn:
        raise DecodeError(*args, parents=parents, expected=tp, actual=thing)

    for decoder in decoders:
        try:
            return cast(Decoder[T], decoder)(
                tp,
                thing,
                strict=strict,
                decoders=decoders,
                parents=new_parents,
            )
        except DecodeError:
            pass

    else:
        origin, args = get_origin(tp), get_args(tp)

        if tp is Any:
            return cast(T, thing)

        elif tp is None:
            if thing is not None:
                throw()
            else:
                return cast(T, thing)

        elif origin is Literal:
            arg, *_ = args
            if thing != arg:
                throw()
            else:
                return cast(T, thing)

        elif origin is Union:
            for member in args:
                try:
                    return decode(
                        member,
                        thing,
                        strict=strict,
                        decoders=decoders,
                        parents=new_parents,
                    )
                except DecodeError:
                    pass
            else:
                throw()

        elif origin in _MAPS:
            if not isinstance(thing, Mapping):
                throw()
            else:
                lhs, rhs = args
                mapping: Mapping[Any, Any] = {
                    decode(
                        lhs,
                        k,
                        strict=strict,
                        decoders=decoders,
                        parents=new_parents,
                    ): decode(
                        rhs,
                        v,
                        strict=strict,
                        decoders=decoders,
                        parents=new_parents,
                    )
                    for k, v in thing.items()
                }
                return cast(T, mapping)

        elif origin in _SETS:
            if not isinstance(thing, ABC_Iterable):
                throw()
            else:
                t, *_ = args
                it: Iterator[Any] = (
                    decode(
                        t,
                        item,
                        strict=strict,
                        decoders=decoders,
                        parents=new_parents,
                    )
                    for item in thing
                )
                return cast(T, {*it} if origin in _SETS_M else frozenset(it))

        elif origin in _SEQS:
            if not isinstance(thing, ABC_Iterable):
                throw()
            else:
                t, *_ = args
                it = (
                    decode(
                        t,
                        item,
                        strict=strict,
                        decoders=decoders,
                        parents=new_parents,
                    )
                    for item in thing
                )
                return cast(T, [*it] if origin in _SEQS_M else tuple(it))

        elif origin is tuple:
            if not isinstance(thing, Sequence):
                throw()
            else:
                tps = (
                    chain(args[:-1], repeat(args[-2]))
                    if len(args) >= 2 and args[-1] is Ellipsis
                    else args
                )
                return cast(
                    T,
                    tuple(
                        decode(
                            t,
                            item,
                            strict=strict,
                            decoders=decoders,
                            parents=new_parents,
                        )
                        for t, item in zip(tps, thing)
                    ),
                )

        elif origin and len(args):
            throw()

        elif isclass(tp) and issubclass(tp, Enum):
            if type(thing) is str and hasattr(tp, thing):
                enum = attrgetter(thing)(tp)
                if isinstance(enum, tp):
                    return cast(T, enum)
                else:
                    throw()
            else:
                throw()

        elif is_dataclass(tp):
            if not isinstance(thing, Mapping):
                throw()
            else:
                dc_fields = {field.name: field.type for field in fields(tp)}
                extra_keys = thing.keys() - dc_fields.keys()
                if strict and extra_keys:
                    raise ExtraKeyError(
                        parents=parents, expected=tp, actual=thing, keys=extra_keys
                    )
                else:
                    kwargs: Mapping[str, Any] = {
                        f_name: decode(
                            f_type,
                            thing[f_name],
                            strict=strict,
                            decoders=decoders,
                            parents=new_parents,
                        )
                        for f_name, f_type in dc_fields.items()
                        if f_name in thing
                    }
                    try:
                        return cast(Callable[..., T], tp)(**kwargs)
                    except TypeError as e:
                        throw()

        else:
            ttp = (
                (attrgetter(tp)(builtins) if hasattr(builtins, tp) else None)
                if type(tp) is str
                else tp
            )
            if ttp is None:
                throw()
            elif isinstance(ttp, TypeVar):
                throw()
            elif not isinstance(thing, ttp):
                throw()
            else:
                return cast(T, thing)
