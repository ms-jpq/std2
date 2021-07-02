from __future__ import annotations

from dataclasses import MISSING, fields, is_dataclass
from enum import Enum
from inspect import isclass
from itertools import chain, repeat
from typing import (
    Any,
    Callable,
    Literal,
    Mapping,
    MutableMapping,
    MutableSet,
    Sequence,
    SupportsFloat,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from ..types import is_it
from .coders import DEFAULT_DECODERS
from .types import MAPS, PRIMITIVES, SEQS, SETS, DecodeError, Decoder, DParser, DStep


def _new_parser(
    tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
) -> DParser:
    origin, args = get_origin(tp), get_args(tp)

    if tp is Any:
        return lambda x: (True, x)

    elif tp is None:

        def p(x: Any) -> DStep:
            if x is None:
                return True, None
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return p

    elif origin is Literal:
        a = {*args}

        def p(x: Any) -> DStep:
            if type(x) in PRIMITIVES and x in a:
                return True, x
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return p

    elif origin is Union:
        ps = tuple(
            _new_parser(a, path=path, strict=strict, decoders=decoders) for a in args
        )

        def p(x: Any) -> DStep:
            for succ, y in (p(x) for p in ps):
                if succ:
                    return True, y
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return p

    elif origin in MAPS:
        lp, rp = (
            _new_parser(a, path=path, strict=strict, decoders=decoders) for a in args
        )

        def p(x: Any) -> DStep:
            if not isinstance(x, Mapping):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                acc = {}
                for k, v in x.items():
                    sl, l = lp(k)
                    if not sl:
                        return False, l
                    sr, r = rp(v)
                    if not sr:
                        return False, r

                    acc[l] = r
                else:
                    return True, acc

        return p

    elif origin in SETS:
        a, *_ = args
        pp = _new_parser(a, path=path, strict=strict, decoders=decoders)

        def p(x: Any) -> DStep:
            if not is_it(x):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                acc = set()
                for succ, m in map(pp, x):
                    if succ:
                        acc.add(m)
                    else:
                        return False, m
                else:
                    return True, acc

        return p

    elif origin in SEQS:
        a, *_ = args
        pp = _new_parser(a, path=path, strict=strict, decoders=decoders)

        def p(x: Any) -> DStep:
            if not is_it(x):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                acc = []
                for succ, m in map(pp, x):
                    if succ:
                        acc.append(m)
                    else:
                        return False, m
                else:
                    return True, acc

        return p

    elif origin is tuple:
        if len(args) >= 2 and args[-1] is Ellipsis:
            bp = tuple(
                _new_parser(a, path=path, strict=strict, decoders=decoders)
                for a in args[:-1]
            )
            ep = repeat(
                _new_parser(args[-2], path=path, strict=strict, decoders=decoders)
            )

            def p(x: Any) -> DStep:
                if not is_it(x):
                    return False, DecodeError(path=(*path, tp), actual=x)
                else:
                    acc = []
                    for succ, y in (p(m) for p, m in zip(chain(bp, ep), x)):
                        if succ:
                            acc.append(y)
                        else:
                            return False, y
                    else:
                        return True, acc

        else:
            ps = tuple(
                _new_parser(a, path=path, strict=strict, decoders=decoders)
                for a in args
            )

            def p(x: Any) -> DStep:
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

        return p

    elif origin and args:
        raise ValueError(f"Unexpected type -- {tp}")

    elif isclass(tp) and issubclass(tp, Enum):

        def p(x: Any) -> DStep:
            if not isinstance(x, str):
                return False, DecodeError(path=(*path, tp), actual=x)
            else:
                try:
                    return True, tp[x]
                except KeyError:
                    return False, DecodeError(path=(*path, tp), actual=x)

        return p

    elif is_dataclass(tp):
        hints = get_type_hints(tp, globalns=None, localns=None)
        cls_fields: MutableMapping[str, DParser] = {}
        rq_fields: MutableSet[str] = set()
        for field in fields(tp):
            if field.init:
                fp = _new_parser(
                    hints[field.name],
                    path=(*path, field),
                    strict=strict,
                    decoders=decoders,
                )
                req = field.default is MISSING and field.default_factory is MISSING  # type: ignore
                cls_fields[field.name] = fp
                if req:
                    rq_fields.add(field.name)

        def p(x: Any) -> DStep:
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

        return p

    elif tp is float:

        def p(x: Any) -> DStep:
            if isinstance(x, SupportsFloat):
                return True, x
            else:
                return False, DecodeError(path=(*path, tp), actual=x)

        return p

    else:
        for d in decoders:
            dp = d(tp, path=path, strict=strict, decoders=decoders)
            if dp:
                return dp
        else:

            def p(x: Any) -> DStep:
                if isinstance(x, tp):
                    return True, x
                else:
                    return False, DecodeError(path=(*path, tp), actual=x)

            return p


def new_decoder(
    tp: Any, strict: bool = True, decoders: Sequence[Decoder] = DEFAULT_DECODERS
) -> Callable[[Any], Any]:
    p = _new_parser(tp, path=(), strict=strict, decoders=decoders)

    def parser(x: Any) -> Any:
        ok, thing = p(x)
        if ok:
            return thing
        else:
            raise thing

    return parser

