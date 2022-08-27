from asyncio import FIRST_COMPLETED, wait
from asyncio.exceptions import CancelledError
from asyncio.tasks import Task, create_task
from itertools import count
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Iterable,
    MutableMapping,
    Tuple,
    TypeVar,
    cast,
)

from ._prelude import aiter
from .asyncio import cancel

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


async def merge(*aits: AsyncIterable[_T]) -> AsyncIterator[_T]:
    channels: MutableMapping[Task, AsyncIterator[_T]] = {}

    for ait in aits:
        a = aiter(ait)
        key = create_task(cast(Any, a.__anext__()))
        channels[key] = a

    try:
        while channels:
            done, _ = await wait(channels, return_when=FIRST_COMPLETED)
            for task in done:
                a = channels.pop(task)
                try:
                    item = task.result()
                except StopAsyncIteration:
                    pass
                else:
                    key = create_task(cast(Any, a.__anext__()))
                    channels[key] = a
                    yield item
    except CancelledError:
        await cancel(*channels)
        channels.clear()
        raise

    assert not channels
