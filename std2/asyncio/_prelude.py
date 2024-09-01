import sys
from asyncio import get_running_loop, sleep
from asyncio.futures import Future
from asyncio.locks import Lock
from asyncio.tasks import Task, create_task, gather
from functools import lru_cache, partial, wraps
from logging import Logger
from typing import Any, Awaitable, Callable, Coroutine, Optional, TypeVar, cast

from ..logging import log_exc

_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Coroutine])


async def pure(x: _T) -> _T:
    return x


def go(log: Logger, aw: Awaitable[_T], suppress: bool = False) -> Awaitable[_T]:
    async def wrapped() -> _T:
        with log_exc(log, suppress=suppress):
            return await aw

    return create_task(wrapped())


def cancel(*fs: Future) -> Future:
    for f in fs:
        f.cancel()

    async def cont(f: Future) -> None:
        while not f.done():
            await sleep(0)

    return gather(*map(cont, fs))


def Locker() -> Callable[[], Lock]:
    @lru_cache(maxsize=None)
    def lock() -> Lock:
        return Lock()

    return lock


def Cancellation() -> Callable[[_F], _F]:
    lock = Locker()
    task: Optional[Task] = None

    def cont(fn: _F) -> _F:
        @wraps(fn)
        async def wrapped(*__a: Any, **__kw: Any) -> Any:
            nonlocal task
            async with lock():
                if t := task:
                    await cancel(t)
                t = create_task(fn(*__a, **__kw))
                task = t
            return await t

        return cast(_F, wrapped)

    return cont


if sys.version_info < (3, 9):

    async def to_thread(f: Callable[..., _T], *args: Any, **kwargs: Any) -> _T:
        loop = get_running_loop()
        cont = partial(f, *args, **kwargs)
        return await loop.run_in_executor(None, cont)

else:
    from asyncio.threads import to_thread as _to_thread

    to_thread = _to_thread
