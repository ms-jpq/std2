from asyncio import create_task, sleep
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")

GO = Callable[[T], Awaitable[Awaitable[T]]]


async def go(aw: Awaitable[T]) -> Awaitable[T]:
    task = create_task(aw)
    await sleep(0)
    return task
