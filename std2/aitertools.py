from itertools import count
from typing import AsyncIterable, AsyncIterator, Awaitable, Iterable, Tuple, TypeVar

from ._prelude import aiter

T = TypeVar("T")


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
