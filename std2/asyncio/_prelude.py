import sys
from asyncio import create_task, get_running_loop, sleep
from asyncio.futures import Future
from functools import partial
from logging import Logger
from typing import Any, Awaitable, Callable, TypeVar

from ..logging import log_exc

_T = TypeVar("_T")


async def pure(x: _T) -> _T:
    return x


def go(log: Logger, aw: Awaitable[_T], suppress: bool = False) -> Awaitable[_T]:
    async def wrapped() -> _T:
        with log_exc(log, suppress=suppress):
            return await aw

    return create_task(wrapped())


async def cancel(f: Future) -> None:
    f.cancel()
    while not f.done():
        await sleep(0)


if sys.version_info < (3, 9):

    async def to_thread(f: Callable[..., _T], *args: Any, **kwargs: Any) -> _T:
        loop = get_running_loop()
        cont = partial(f, *args, **kwargs)
        return await loop.run_in_executor(None, cont)

else:
    from asyncio.threads import to_thread as _to_thread

    to_thread = _to_thread
