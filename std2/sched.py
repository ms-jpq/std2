from asyncio import sleep
from typing import AsyncIterator

from .timeit import timeit


async def ticker(period: float, immediately: bool = True) -> AsyncIterator[float]:
    elapsed = 0.0
    if immediately:
        with timeit() as tt:
            yield 0.0, elapsed
        elapsed = tt()

    while True:
        delay = max(period - elapsed, 0)
        await sleep(delay)
        with timeit() as tt:
            yield delay, elapsed
        elapsed = tt()
