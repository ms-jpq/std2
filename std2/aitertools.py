from itertools import count
from typing import (
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Iterable,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from .types import Void, VoidType

T = TypeVar("T")
U = TypeVar("U")


def aiter(ait: AsyncIterable[T]) -> AsyncIterator[T]:
    return ait.__aiter__()


async def anext(
    ait: AsyncIterator[T], default: Union[U, VoidType] = Void
) -> Union[T, U]:
    if default is Void:
        return await ait.__anext__()
    else:
        try:
            return await ait.__anext__()
        except StopAsyncIteration:
            return cast(U, default)


async def to_async(it: Iterable[T]) -> AsyncIterator[T]:
    for item in it:
        yield item


async def aiterify(aws: Iterable[Awaitable[T]]) -> AsyncIterator[T]:
    for aw in aws:
        yield await aw


async def aenumerate(
    ait: AsyncIterable[T], start: int = 0
) -> AsyncIterator[Tuple[int, T]]:
    it = count(start)
    async for item in ait:
        yield next(it), item


async def atake(ait: AsyncIterable[T], n: int) -> AsyncIterator[T]:
    ch = aiter(ait)
    for _ in range(n):
        try:
            yield await ch.__anext__()
        except StopAsyncIteration:
            break


async def achain(*aits: AsyncIterable[T]) -> AsyncIterator[T]:
    for ait in aits:
        async for item in ait:
            yield item

