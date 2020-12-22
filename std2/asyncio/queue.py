from asyncio.queues import Queue
from typing import AsyncIterator, TypeVar

T = TypeVar("T")


async def to_iter(queue: Queue[T]) -> AsyncIterator:
    while True:
        yield await queue.get()
