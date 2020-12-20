from typing import Awaitable, Callable, TypeVar, Protocol, Any
from asyncio import create_task

T = TypeVar("T")


class GO(Protocol):
    def __call__(
        self, aw: Awaitable[T], *args: Any, **kwds: Any
    ) -> Awaitable[Awaitable[T]]:
        ...


async def _default_sch(aw: Awaitable[T], *args: Any, **kwds: Any) -> Awaitable[T]:
    return create_task(aw)


_go: GO = _default_sch


async def go(aw: Awaitable[T], *args: Any, **kwds: Any) -> Awaitable[T]:
    return await _go(aw, *args, **kwds)


def set_scheduler(go: GO) -> None:
    global _go
    _go = go