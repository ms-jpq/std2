from asyncio import FIRST_COMPLETED, Queue, gather, wait
from asyncio.exceptions import CancelledError
from asyncio.locks import Event
from asyncio.tasks import Task, create_task
from itertools import count
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Iterable,
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


async def _merge_helper(q: Queue, end: Task, ait: AsyncIterable[Any]) -> None:
    ch = aiter(ait)

    while True:
        pending_take = create_task(cast(Any, ch.__anext__()))
        done_1, _ = await wait((end, pending_take), return_when=FIRST_COMPLETED)

        if pending_take in done_1:
            try:
                item = await pending_take
            except StopAsyncIteration:
                break
            else:
                if end in done_1:
                    break
                else:
                    pending_put = create_task(q.put(item))
                    done_2, _ = await wait(
                        (end, pending_put), return_when=FIRST_COMPLETED
                    )

                    if pending_put in done_2:
                        await pending_put

                    if end in done_2:
                        break

        if end in done_1:
            break


async def merge(*aits: AsyncIterable[_T]) -> AsyncIterator[_T]:
    ev = Event()
    q: Queue = Queue(maxsize=1)

    end = create_task(ev.wait())
    g = gather(*(_merge_helper(q, end=end, ait=ait) for ait in aits))

    try:
        while True:
            fut = create_task(q.get())
            done, _ = await wait((g, fut), return_when=FIRST_COMPLETED)
            if fut in done:
                item = await fut
                yield item

            if g in done:
                break
    except CancelledError:
        await cancel(g)
    finally:
        ev.set()
        await g
