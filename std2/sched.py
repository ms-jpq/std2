from asyncio import sleep
from typing import AsyncIterator, Tuple

from .timeit import timeit


async def ticker(
    period: float, immediately: bool = True
) -> AsyncIterator[Tuple[float, float]]:
    elapsed = 0.0
    if immediately:
        with timeit() as duration:
            yield 0.0, elapsed
        elapsed = duration()

    while True:
        delay = max(period - elapsed, 0)
        await sleep(delay)
        with timeit() as duration:
            yield delay, elapsed
        elapsed = duration()
