from asyncio.queues import Queue
from typing import Any, AsyncIterator


async def to_iter(queue: Queue) -> AsyncIterator[Any]:
    while True:
        yield await queue.get()
