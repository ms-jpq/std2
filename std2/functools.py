from functools import wraps
from typing import Any, Callable, TypeVar, cast

from .types import AnyFun

_T = TypeVar("_T")
_U = TypeVar("_U")
_F = TypeVar("_F", bound=Callable)


def once(f: _F) -> _F:
    done, ret = False, None

    @wraps(f)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        nonlocal done, ret
        if done:
            return ret
        else:
            ret = f(*args, **kwargs)
            done = True
            return ret

    return cast(_F, wrapped)


def constantly(thing: _T) -> AnyFun[_T]:
    def f(*_: Any, **__: Any) -> _T:
        return thing

    return f


def identity(thing: _T, *_: Any, **__: Any) -> _T:
    return thing


async def apure(item: _T, apply: Callable[[_T], _U]) -> _U:
    return apply(item)
