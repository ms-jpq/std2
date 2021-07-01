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
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from ..types import is_it
from .coders import DEFAULT_ENCODERS
from .types import MAPS, SEQS, SETS, Encoder, EncoderError, EParser, EStep


def _new_parser(tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]) -> EParser:
    origin, args = get_origin(tp), get_args(tp)

    if tp is Any:
        return lambda x: (True, x)

    elif tp is None:

        def p(x: Any) -> EStep:
            if x is None:
                return True, None
            else:
                return False, EncoderError(path=(*path, tp), actual=x)

        return p

    elif origin is Literal:
        a = {*args}

        def p(x: Any) -> EStep:
            if x in a:
                return True, x
            else:
                return False, EncoderError(path=(*path, tp), actual=x)

        return p

    elif origin is Union:
        ps = tuple(_new_parser(a, path=path, encoders=encoders) for a in args)

        def p(x: Any) -> EStep:
            for succ, y in (p(x) for p in ps):
                if succ:
                    return True, y
            else:
                return False, EncoderError(path=(*path, tp), actual=x)

        return p

    elif origin in MAPS:
        lp, rp = (_new_parser(a, path=path, encoders=encoders) for a in args)

        def p(x: Any) -> EStep:
            if not isinstance(x, Mapping):
                return False, EncoderError(path=(*path, tp), actual=x)
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
        pp = _new_parser(a, path=path, encoders=encoders)

        def p(x: Any) -> EStep:
            if not is_it(x):
                return False, EncoderError(path=(*path, tp), actual=x)
            else:
                acc = {}
                for succ, m in map(pp, x):
                    if succ:
                        acc[m] = True
                    else:
                        return False, m
                else:
                    return False, EncoderError(path=(*path, tp), actual=x)

        return p

    elif origin in SEQS:
        a, *_ = args
        pp = _new_parser(a, path=path, encoders=encoders)

        def p(x: Any) -> EStep:
            if not is_it(x):
                return False, EncoderError(path=(*path, tp), actual=x)
            else:
                acc = []
                for succ, m in map(p, x):
                    if succ:
                        acc.append(m)
                    else:
                        return False, m
                else:
                    return True, acc

        return p

    elif origin is tuple:
        if len(args) >= 2 and args[-1] is Ellipsis:
            bp = tuple(_new_parser(a, path=path, encoders=encoders) for a in args[:-1])
            ep = repeat(_new_parser(args[-2], path=path, encoders=encoders))

            def p(x: Any) -> EStep:
                if not is_it(x):
                    return False, EncoderError(path=(*path, tp), actual=x)
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
            ps = tuple(_new_parser(a, path=path, encoders=encoders) for a in args)

            def p(x: Any) -> EStep:
                if not is_it(x):
                    return False, EncoderError(path=(*path, tp), actual=x)
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

        def p(x: Any) -> EStep:
            if not isinstance(x, Enum):
                return False, EncoderError(path=(*path, tp), actual=x)
            else:
                return True, x.name

        return p

    elif is_dataclass(tp):
        hints = get_type_hints(tp, globalns=None, localns=None)
        cls_fields: MutableMapping[str, EParser] = {}
        rq_fields: MutableSet[str] = set()
        for field in fields(tp):
            if field.init:
                fp = _new_parser(hints[field.name], path=path, encoders=encoders)
                req = field.default is MISSING and field.default_factory is MISSING  # type: ignore
                cls_fields[field.name] = fp
                if req:
                    rq_fields.add(field.name)

        def p(x: Any) -> EStep:
            if not is_dataclass(x):
                return False, EncoderError(path=(*path, tp), actual=x)
            else:
                acc: MutableMapping[str, Any] = {}
                for k, p in cls_fields.items():
                    if hasattr(x, k):
                        succ, v = p(getattr(x, k))
                        if succ:
                            acc[k] = v
                        else:
                            return False, v
                    elif req:
                        return False, EncoderError(
                            path=(*path, tp), actual=x, missing_keys=k
                        )

                return True, acc

        return p

    else:
        for e in encoders:
            epp = e(tp, path=path, encoders=encoders)
            if epp:
                return epp
        else:

            def p(x: Any) -> EStep:
                if isinstance(x, tp):
                    return True, x
                else:
                    return False, EncoderError(path=(*path, tp), actual=x)

            return p


def new_encoder(
    tp: Any, encoders: Sequence[Encoder] = DEFAULT_ENCODERS
) -> Callable[[Any], Any]:
    p = _new_parser(tp, path=(), encoders=encoders)

    def parser(x: Any) -> Any:
        ok, thing = p(x)
        if ok:
            return thing
        else:
            raise thing

    return parser

