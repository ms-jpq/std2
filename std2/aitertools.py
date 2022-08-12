from asyncio import FIRST_COMPLETED, Queue, gather, wait
from asyncio.locks import Event
from asyncio.tasks import Task, create_task
from itertools import count
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Iterable,
    MutableSequence,
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


async def _merge_helper(
    cancel_when_done: bool, q: Queue, end: Task, ait: AsyncIterable[Any]
) -> None:
    ch = aiter(ait)

    try:
        while True:
            pending_take = create_task(cast(Any, ch.__anext__()))
            done_1, pending_1 = await wait(
                (end, pending_take), return_when=FIRST_COMPLETED
            )
            if end in done_1:
                if cancel_when_done:
                    await cancel(*pending_1)
                break
            elif pending_take in done_1:
                try:
                    item = pending_take.result()
                except StopAsyncIteration:
                    break
                else:
                    pending_put = create_task(q.put(item))
                    done_2, pending_2 = await wait(
                        (end, pending_put), return_when=FIRST_COMPLETED
                    )
                    if end in done_2:
                        if cancel_when_done:
                            await cancel(*pending_2)
                        break
                    elif pending_put in done_2:
                        pending_put.result()
                    else:
                        assert False

            else:
                assert False
    finally:
        if isinstance(ch, AsyncGenerator):
            ch.aclose()


async def merge(
    *aits: AsyncIterable[_T], cancel_when_done: bool = False
) -> AsyncIterator[_T]:
    ev = Event()
    stack: MutableSequence[Task] = []
    q: Queue = Queue(maxsize=1)

    end = create_task(ev.wait())
    g = gather(
        *(_merge_helper(cancel_when_done, q=q, end=end, ait=ait) for ait in aits)
    )

    try:
        while True:
            fut = stack.pop() if stack else create_task(q.get())
            done, pending = await wait((g, fut), return_when=FIRST_COMPLETED)

            if fut in done:
                yield fut.result()
            elif fut in pending:
                stack.append(fut)

            if g in done:
                await cancel(*pending)
                break
    finally:
        ev.set()
        await g
