from itertools import count
from typing import AsyncIterable, AsyncIterator, Iterable, Tuple, TypeVar

T = TypeVar("T")


async def to_async(it: Iterable[T]) -> AsyncIterator[T]:
    for item in it:
        yield item


async def aenumerate(
    ait: AsyncIterable[T], start: int = 0
) -> AsyncIterator[Tuple[int, T]]:
    it = count(start)
    async for item in ait:
        yield next(it), item
