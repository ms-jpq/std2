from typing import Any, Callable, TypeVar

from .types import AnyFun

T = TypeVar("T")
U = TypeVar("U")


def constantly(thing: T) -> AnyFun[T]:
    def f(*args: Any, **kwargs: Any) -> T:
        return thing

    return f


def identity(thing: T, *args: Any, **kwargs: Any) -> T:
    return thing


async def apure(item: T, apply: Callable[[T], U]) -> U:
    return apply(item)
