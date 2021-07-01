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
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from ..types import is_it
from .decoder import DecodeError

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


_MAPS_M = {MutableMapping, ABC_MutableMapping, Dict, dict}
_MAPS = {Mapping, ABC_Mapping} | _MAPS_M

_SETS_M = {MutableSet, ABC_MutableSet, Set, set}
_SETS = {AbstractSet, ABC_Set, FrozenSet, frozenset} | _SETS_M

_SEQS_M = {MutableSequence, ABC_MutableSequence, List, list}
_SEQS = {Sequence, ABC_Sequence} | _SEQS_M


Step = Tuple[bool, Any]
Parser = Callable[[Any], Step]


def _new_parser(tp: Any) -> Parser:
    origin, args = get_origin(tp), get_args(tp)

    if tp is Any:
        return lambda x: (True, x)
    elif tp is None:
        return lambda x: (x is None, None)
    elif origin is Literal:
        a = frozenset(args)
        return lambda x: (x in a, x)
    elif origin is Union:
        parsers = tuple(map(_new_parser, args))

        def parser(x: Any) -> Step:
            for p in parsers:
                succ, y = p(x)
                if succ:
                    return True, y
            else:
                return False, None

        return parser

    elif origin in _MAPS:
        kp, vp = map(_new_parser, args)

        def parser(x: Any) -> Step:
            if not isinstance(x, Mapping):
                return False, None
            else:
                acc = {}
                for k, v in x.items():
                    (sl, l), (sr, r) = kp(k), vp(v)
                    if sl and sr:
                        acc[l] = r
                    else:
                        return False, None
                else:
                    return True, acc

        return parser

    elif origin in _SETS:
        mp, *_ = map(_new_parser, args)

        def parser(x: Any) -> Step:
            if not is_it(x):
                return False, None
            else:
                acc = set()
                for succ, m in map(mp, x):
                    if succ:
                        acc.add(m)
                    else:
                        return False, None
                else:
                    return True, acc

        return parser

    elif origin in _SEQS:
        mp, *_ = map(_new_parser, args)

        def parser(x: Any) -> Step:
            if not is_it(x):
                return False, None
            else:
                acc = []
                for succ, m in map(mp, x):
                    if succ:
                        acc.append(m)
                    else:
                        return False, None
                else:
                    return True, acc

        return parser

    elif origin is tuple:
        if len(args) >= 2 and args[-1] is Ellipsis:
            b_parsers = tuple(map(_new_parser, args[:-1]))
            e_parsers = repeat(_new_parser(args[-1]))

            def parser(x: Any) -> Step:
                if not is_it(x):
                    return False, None
                else:
                    acc = []
                    for succ, y in (
                        p(m) for p, m in zip(chain(b_parsers, e_parsers), x)
                    ):
                        if succ:
                            acc.append(y)
                        else:
                            return False, None
                    else:
                        return True, acc

        else:
            parsers = tuple(map(_new_parser, args))

            def parser(x: Any) -> Step:
                if not is_it(x):
                    return False, None
                else:
                    acc = []
                    for succ, y in (p(m) for p, m in zip(parsers, x)):
                        if succ:
                            acc.append(y)
                        else:
                            return False, None
                    else:
                        return True, acc

        return parser

    elif origin and args:
        raise ValueError(f"Unexpected type -- {tp}")

    elif isclass(tp) and issubclass(tp, Enum):

        def parser(x: Any) -> Step:
            if not isinstance(x, str):
                return False, None
            else:
                try:
                    return True, tp[x]
                except KeyError:
                    return False, None

        return parser

    elif is_dataclass(tp):
        hints = get_type_hints(tp, globalns=None, localns=None)
        cls_fields: MutableMapping[str, Tuple[bool, Parser]] = {}
        for field in fields(tp):
            if field.init:
                req = field.default is MISSING and field.default_factory is MISSING  # type: ignore
                cls_fields[field.name] = req, _new_parser(hints[field.name])

        def parser(x: Any) -> Step:
            if not isinstance(x, Mapping):
                return False, None
            else:
                kwargs: MutableMapping[str, Any] = {}
                for k, (req, p) in cls_fields.items():
                    if k in x:
                        succ, v = p(x[k])
                        if succ:
                            kwargs[k] = v
                        else:
                            return False, None
                    elif req:
                        return False, None

                return True, tp(**kwargs)

        return parser
    elif tp is float:
        return lambda x: (True, x) if isinstance(x, SupportsFloat) else (False, None)

    else:
        return lambda x: (True, x) if isinstance(x, tp) else (False, None)


def new_parser(tp: Any) -> Callable[[Any], Any]:
    p = _new_parser(tp)

    def parser(x: Any) -> Any:
        ok, thing = p(x)
        if ok:
            return thing
        else:
            raise DecodeError(path="", actual="")

    return parser

