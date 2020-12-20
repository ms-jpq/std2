from asyncio import create_task
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")

GO = Callable[[T], Awaitable[Awaitable[T]]]


async def go(aw: Awaitable[T]) -> Awaitable[T]:
    return create_task(aw)
