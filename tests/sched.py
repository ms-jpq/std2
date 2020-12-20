from asyncio import sleep
from unittest import IsolatedAsyncioTestCase

from ..std2.aitertools import aenumerate
from ..std2.sched import ticker
from ._consts import SMOL_REP_FACTOR


class Ticker(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        period = 0.3
        slep = 0.1
        async for i, (delay, elapsed), in aenumerate(
            ticker(period, immediately=True),
        ):
            if i == SMOL_REP_FACTOR:
                break

            await sleep(slep)

            if i:
                self.assertAlmostEqual(delay, period - slep, places=1)
                self.assertAlmostEqual(elapsed, slep, places=1)
            else:
                self.assertAlmostEqual(delay, 0)
                self.assertAlmostEqual(elapsed, 0)

    async def test_2(self) -> None:
        period = 0.3
        slep = 0.1
        async for i, (delay, elapsed), in aenumerate(
            ticker(period, immediately=False),
        ):
            if i == SMOL_REP_FACTOR:
                break

            await sleep(slep)

            if i:
                self.assertAlmostEqual(delay, period - slep, places=1)
                self.assertAlmostEqual(elapsed, slep, places=1)
            else:
                self.assertAlmostEqual(delay, period)
                self.assertAlmostEqual(elapsed, 0)

    async def test_3(self) -> None:
        period = 0.1
        slep = 0.3
        async for i, (delay, elapsed), in aenumerate(
            ticker(period, immediately=True),
        ):
            if i == SMOL_REP_FACTOR:
                break

            await sleep(slep)

            if i:
                self.assertAlmostEqual(delay, 0, places=1)
                self.assertAlmostEqual(elapsed, slep, places=1)
            else:
                self.assertAlmostEqual(delay, 0)
                self.assertAlmostEqual(elapsed, 0)
