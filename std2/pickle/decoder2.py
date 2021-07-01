from __future__ import annotations

from collections.abc import Mapping as ABC_Mapping
from collections.abc import MutableMapping as ABC_MutableMapping
from collections.abc import MutableSequence as ABC_MutableSequence
from collections.abc import MutableSet as ABC_MutableSet
from collections.abc import Sequence as ABC_Sequence
from collections.abc import Set as ABC_Set
from dataclasses import MISSING, fields, is_dataclass
from enum import Enum
from inspect import isclass
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
    List,
    Literal,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Set,
    SupportsFloat,
    Tuple,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from ..types import is_it
from .decoder import DecodeError

_MAPS_M = {MutableMapping, ABC_MutableMapping, Dict, dict}
_MAPS = {Mapping, ABC_Mapping} | _MAPS_M

_SETS_M = {MutableSet, ABC_MutableSet, Set, set}
_SETS = {AbstractSet, ABC_Set, FrozenSet, frozenset} | _SETS_M

_SEQS_M = {MutableSequence, ABC_MutableSequence, List, list}
_SEQS = {Sequence, ABC_Sequence} | _SEQS_M


Step = Tuple[Literal[False, True], Union[DecodeError, Any]]
Parser = Callable[[Any], Step]

Parsers = Mapping[Callable[[Any], bool], Parser]


def _new_parser(tp: Any, path: Sequence[Any], strict: bool) -> Parser:
    origin, args = get_origin(tp), get_args(tp)

    if tp is Any:
        return lambda x: (True, x)
    elif tp is None:

        def parser(x: Any) -> Step:
            if x is None:
                return True, None
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return parser
    elif origin is Literal:
        a = {*args}

        def parser(x: Any) -> Step:
            if x in a:
                return True, x
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return parser

    elif origin is Union:
        ps = tuple(_new_parser(a, path=path, strict=strict) for a in args)

        def parser(x: Any) -> Step:
            for succ, y in (p(x) for p in ps):
                if succ:
                    return True, y
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return parser

    elif origin in _MAPS:
        kp, vp = (_new_parser(a, path=path, strict=strict) for a in args)

        def parser(x: Any) -> Step:
            if not isinstance(x, Mapping):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                acc = {}
                for k, v in x.items():
                    sl, l = kp(k)
                    if not sl:
                        return False, l
                    sr, r = vp(v)
                    if not sr:
                        return False, r

                    acc[l] = r
                else:
                    return True, acc

        return parser

    elif origin in _SETS:
        p, *_ = (_new_parser(a, path=path, strict=strict) for a in args)

        def parser(x: Any) -> Step:
            if not is_it(x):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                acc = set()
                for succ, m in map(p, x):
                    if succ:
                        acc.add(m)
                    else:
                        return False, m
                else:
                    return False, DecodeError(path=(*path, tp), actual=x)

        return parser

    elif origin in _SEQS:
        p, *_ = (_new_parser(a, path=path, strict=strict) for a in args)

        def parser(x: Any) -> Step:
            if not is_it(x):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                acc = []
                for succ, m in map(p, x):
                    if succ:
                        acc.append(m)
                    else:
                        return False, m
                else:
                    return True, acc

        return parser

    elif origin is tuple:
        if len(args) >= 2 and args[-1] is Ellipsis:
            b_parsers = tuple(
                _new_parser(a, path=path, strict=strict) for a in args[:-1]
            )
            e_parsers = repeat(_new_parser(args[-2], path=path, strict=strict))

            def parser(x: Any) -> Step:
                if not is_it(x):
                    return False, DecodeError(path=(*path, tp), actual=x)
                else:
                    acc = []
                    for succ, y in (
                        p(m) for p, m in zip(chain(b_parsers, e_parsers), x)
                    ):
                        if succ:
                            acc.append(y)
                        else:
                            return False, y
                    else:
                        return True, acc

        else:
            ps = tuple(_new_parser(a, path=path, strict=strict) for a in args)

            def parser(x: Any) -> Step:
                if not is_it(x):
                    return False, DecodeError(path=(*path, tp), actual=x)
                else:
                    acc = []
                    for succ, y in (p(m) for p, m in zip(ps, x)):
                        if succ:
                            acc.append(y)
                        else:
                            return False, y
                    else:
                        return True, acc

        return parser

    elif origin and args:
        raise ValueError(f"Unexpected type -- {tp}")

    elif isclass(tp) and issubclass(tp, Enum):

        def parser(x: Any) -> Step:
            if not isinstance(x, str):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                try:
                    return True, tp[x]
                except KeyError:
                    return False, DecodeError(path=(*path, tp), actual=x)

        return parser

    elif is_dataclass(tp):
        hints = get_type_hints(tp, globalns=None, localns=None)
        cls_fields: MutableMapping[str, Parser] = {}
        rq_fields: MutableSet[str] = set()
        for field in fields(tp):
            if field.init:
                p = _new_parser(hints[field.name], path=path, strict=strict)
                req = field.default is MISSING and field.default_factory is MISSING  # type: ignore
                cls_fields[field.name] = p
                if req:
                    rq_fields.add(field.name)

        def parser(x: Any) -> Step:
            if not isinstance(x, Mapping):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                kwargs: MutableMapping[str, Any] = {}
                for k, p in cls_fields.items():
                    if k in x:
                        succ, v = p(x[k])
                        if succ:
                            kwargs[k] = v
                        else:
                            return False, v
                    elif req:
                        return False, DecodeError(
                            path=(*path, tp), actual=x, missing_keys=k
                        )

                ks = kwargs.keys()
                mk = rq_fields - ks
                if mk:
                    return False, DecodeError(
                        path=(*path, tp), actual=x, missing_keys=mk
                    )

                if strict:
                    ek = x.keys() - ks
                    if ek:
                        return False, DecodeError(
                            path=(*path, tp), actual=x, extra_keys=ek
                        )

                return True, tp(**kwargs)

        return parser
    elif tp is float:

        def parser(x: Any) -> Step:
            if isinstance(x, SupportsFloat):
                return True, x
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return parser
    else:

        def parser(x: Any) -> Step:
            if isinstance(x, tp):
                return True, x
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return parser


def new_parser(tp: Any, strict: bool = True) -> Callable[[Any], Any]:
    p = _new_parser(tp, path=(), strict=strict)

    def parser(x: Any) -> Any:
        ok, thing = p(x)
        if ok:
            return thing
        else:
            raise thing

    return parser

