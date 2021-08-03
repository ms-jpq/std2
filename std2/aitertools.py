from itertools import count
from typing import AsyncIterable, AsyncIterator, Awaitable, Iterable, Tuple, TypeVar

from ._prelude import aiter

_T = TypeVar("_T")


async def to_async(it: Iterable[_T]) -> AsyncIterator[_T]:
    for item in it:
        yield item


async def aiterify(aws: Iterable[Awaitable[_T]]) -> AsyncIterator[_T]:
    for aw in aws:
        yield await aw


async def aenumerate(
    ait: AsyncIterable[_T], start: int = 0
) -> AsyncIterator[Tuple[int, _T]]:
    it = count(start)
    async for item in ait:
        yield next(it), item


async def atake(ait: AsyncIterable[_T], n: int) -> AsyncIterator[_T]:
    ch = aiter(ait)
    for _ in range(n):
        try:
            yield await ch.__anext__()
        except StopAsyncIteration:
            break


async def achain(*aits: AsyncIterable[_T]) -> AsyncIterator[_T]:
    for ait in aits:
        async for item in ait:
            yield item
