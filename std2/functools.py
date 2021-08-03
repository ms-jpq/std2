from typing import Any, Callable, TypeVar, cast

from .types import AnyFun

T = TypeVar("T")
U = TypeVar("U")
F = TypeVar("F", bound=Callable)


def once(f: F) -> F:
    done, ret = False, None

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        nonlocal done, ret
        if done:
            return ret
        else:
            ret = f(*args, **kwargs)
            done = True
            return ret

    return cast(F, wrapped)


def constantly(thing: T) -> AnyFun[T]:
    def f(*_: Any, **__: Any) -> T:
        return thing

    return f


def identity(thing: T, *_: Any, **__: Any) -> T:
    return thing


async def apure(item: T, apply: Callable[[T], U]) -> U:
    return apply(item)
