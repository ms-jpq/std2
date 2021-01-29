from __future__ import annotations

from collections.abc import Mapping as ABC_Mapping
from collections.abc import MutableMapping as ABC_MutableMapping
from collections.abc import MutableSequence as ABC_MutableSequence
from collections.abc import MutableSet as ABC_MutableSet
from collections.abc import Sequence as ABC_Sequence
from collections.abc import Set as ABC_Set
from dataclasses import MISSING, Field, fields, is_dataclass
from enum import Enum
from itertools import chain, repeat
from locale import strxfrm
from os import linesep
from pprint import pformat
from typing import (
    AbstractSet,
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
    SupportsFloat,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from ..types import is_it

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


_MAPS_M = {MutableMapping, ABC_MutableMapping, Dict, dict}
_MAPS = {Mapping, ABC_Mapping} | _MAPS_M

_SETS_M = {MutableSet, ABC_MutableSet, Set, set}
_SETS = {AbstractSet, ABC_Set, FrozenSet, frozenset} | _SETS_M

_SEQS_M = {MutableSequence, ABC_MutableSequence, List, list}
_SEQS = {Sequence, ABC_Sequence} | _SEQS_M


def _is_optional(field: Field) -> bool:
    return field.default is MISSING and field.default_factory is MISSING  # type: ignore


def _pprn(thingy: Any) -> str:
    if is_dataclass(thingy):
        fs = sorted(fields(thingy), key=lambda f: strxfrm(f.name))
        listed = ", ".join(map(_pprn, fs))
        return f"key of: [ {listed} ]"
    elif isinstance(thingy, Field):
        return f"{thingy.name}: {thingy.type}"
    elif issubclass(thingy, Enum):
        members = tuple(member.name for member in thingy)
        listed = ", ".join(members)
        return f"one of: {{ {listed} }}"
    else:
        return str(thingy)


class DecodeError(Exception):
    def __init__(
        self,
        *args: Any,
        path: Sequence[Any],
        actual: Any,
        missing_keys: Sequence[str] = (),
        extra_keys: Sequence[str] = (),
    ) -> None:
        super().__init__(*args)
        self.path, self.actual = path, actual
        self.missing_keys, self.extra_keys = missing_keys, extra_keys

    def __str__(self) -> str:
        path = f"{linesep}->{linesep}".join(map(_pprn, self.path))
        missing = ", ".join(self.missing_keys)
        extra = ", ".join(self.extra_keys)
        args = ", ".join(map(str, self.args))
        actual = pformat(self.actual, indent=2)
        l1 = f"Path:{linesep}{path}"
        l2 = f"Actual:{linesep}{actual}"
        l3 = f"Missing Keys: {{{missing}}}"
        l4 = f"Extra Keys:   {{{extra}}}"
        l5 = f"Args:         ({args})"
        return (linesep * 2).join((linesep, l1, l2, l3, l4, l5))


class Decoder(Protocol[T_co]):
    def __call__(
        self,
        tp: Any,
        thing: Any,
        strict: bool,
        decoders: Decoders,
        path: Sequence[Any],
    ) -> T_co:
        ...


Decoders = Sequence[Decoder[Any]]


def decode(
    tp: Any,
    thing: Any,
    strict: bool = True,
    decoders: Decoders = (),
    path: Sequence[Any] = (),
) -> T:
    new_path = (*path, tp)

    def throw(
        *args: Any, missing: Sequence[str] = (), extra: Sequence[str] = ()
    ) -> NoReturn:
        raise DecodeError(
            *args, path=new_path, actual=thing, missing_keys=missing, extra_keys=extra
        )

    for decoder in decoders:
        try:
            return cast(Decoder[T], decoder)(
                tp,
                thing,
                strict=strict,
                decoders=decoders,
                path=new_path,
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
            if thing not in args:
                throw()
            else:
                return cast(T, thing)

        elif origin is Union:
            errs: MutableSequence[Exception] = []
            for member in args:
                try:
                    return decode(
                        member,
                        thing,
                        strict=strict,
                        decoders=decoders,
                        path=new_path,
                    )
                except DecodeError as e:
                    errs.append(e)
            else:
                throw(*errs)

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
                        path=new_path,
                    ): decode(
                        rhs,
                        v,
                        strict=strict,
                        decoders=decoders,
                        path=new_path,
                    )
                    for k, v in thing.items()
                }
                return cast(T, mapping)

        elif origin in _SETS:
            if not is_it(thing):
                throw()
            else:
                t, *_ = args
                it: Iterator[Any] = (
                    decode(
                        t,
                        item,
                        strict=strict,
                        decoders=decoders,
                        path=new_path,
                    )
                    for item in thing
                )
                return cast(T, {*it} if origin in _SETS_M else frozenset(it))

        elif origin in _SEQS:
            if not is_it(thing):
                throw()
            else:
                t, *_ = args
                it = (
                    decode(
                        t,
                        item,
                        strict=strict,
                        decoders=decoders,
                        path=new_path,
                    )
                    for item in thing
                )
                return cast(T, [*it] if origin in _SEQS_M else tuple(it))

        elif origin is tuple:
            if not is_it(thing):
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
                            path=new_path,
                        )
                        for t, item in zip(tps, thing)
                    ),
                )

        elif origin and len(args):
            throw()

        elif issubclass(tp, Enum):
            if not isinstance(thing, str):
                throw()
            else:
                try:
                    return cast(T, tp[thing])
                except KeyError as e:
                    throw()

        elif is_dataclass(tp):
            if not isinstance(thing, Mapping):
                throw()

            else:
                hints = get_type_hints(tp, globalns=None, localns=None)
                dc_fields: MutableMapping[str, Tuple[Type, Field]] = {}
                required: MutableSet[str] = set()
                for field in fields(tp):
                    if field.init:
                        dc_fields[field.name] = hints[field.name], field
                        if _is_optional(field):
                            required.add(field.name)

                missing_keys = required - thing.keys()
                extra_keys = thing.keys() - dc_fields.keys()

                if missing_keys or (strict and extra_keys):
                    throw(
                        missing=sorted(missing_keys, key=strxfrm),
                        extra=sorted(extra_keys, key=strxfrm),
                    )

                else:
                    kwargs: Mapping[str, Any] = {
                        f_name: decode(
                            f_type,
                            thing[f_name],
                            strict=strict,
                            decoders=decoders,
                            path=tuple((*new_path, field)),
                        )
                        for f_name, (f_type, field) in dc_fields.items()
                        if f_name in thing
                    }
                    return cast(Callable[..., T], tp)(**kwargs)

        elif tp is float:
            if not isinstance(thing, SupportsFloat):
                throw()
            else:
                return cast(T, thing)

        else:
            if isinstance(tp, TypeVar):
                throw()
            elif not isinstance(thing, tp):
                throw()
            else:
                return cast(T, thing)
