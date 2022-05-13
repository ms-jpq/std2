from asyncio import sleep as asleep
from time import sleep
from typing import AsyncIterator, Iterator, Tuple

from .timeit import timeit


def ticker(period: float, immediately: bool = True) -> Iterator[Tuple[float, float]]:
    elapsed = 0.0
    if immediately:
        with timeit() as duration:
            yield 0.0, elapsed
        elapsed = duration().total_seconds()

    while True:
        delay = max(period - elapsed, 0)
        sleep(delay)
        with timeit() as duration:
            yield delay, elapsed
        elapsed = duration().total_seconds()


async def aticker(
    period: float, immediately: bool = True
) -> AsyncIterator[Tuple[float, float]]:
    elapsed = 0.0
    if immediately:
        with timeit() as duration:
            yield 0.0, elapsed
        elapsed = duration().total_seconds()

    while True:
        delay = max(period - elapsed, 0)
        await asleep(delay)
        with timeit() as duration:
            yield delay, elapsed
        elapsed = duration().total_seconds()
