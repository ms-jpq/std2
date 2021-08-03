from asyncio import create_task, get_running_loop, sleep
from asyncio.futures import Future
from asyncio.tasks import FIRST_COMPLETED, wait
from functools import partial
from logging import Logger
from typing import (
    AbstractSet,
    Any,
    Awaitable,
    Callable,
    MutableSet,
    Tuple,
    TypeVar,
    cast,
)

from ..logging import with_tracking

T = TypeVar("T")
_T2 = TypeVar("_T2", bound=Future)


async def pure(x: T) -> T:
    return x


def go(log: Logger, aw: Awaitable[T], suppress: bool = False) -> Awaitable[T]:
    async def wrapped() -> T:
        with with_tracking(log, suppress=suppress):
            return await aw

    return create_task(wrapped())


async def cancel(f: Future) -> None:
    f.cancel()
    while not f.done():
        await sleep(0)


async def race(aw: _T2, *aws: _T2) -> Tuple[_T2, AbstractSet[_T2], AbstractSet[_T2]]:
    done, pending = await wait((aw, *aws), return_when=FIRST_COMPLETED)
    ret = done.pop()
    return ret, done, pending


async def run_in_executor(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = get_running_loop()
    cont = partial(f, *args, **kwargs)
    return await loop.run_in_executor(None, cont)
