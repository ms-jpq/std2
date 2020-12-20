from asyncio import sleep
from unittest import IsolatedAsyncioTestCase
from ..std2.aitertools import aenumerate
from ..std2.sched import ticker
from ._consts import SMOL_REP_FACTOR


class TimeIt(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        period = 0.2
        async for i, (delay, elapsed), in aenumerate(
            ticker(period, immediately=True), 1
        ):
            if i == SMOL_REP_FACTOR:
                break
