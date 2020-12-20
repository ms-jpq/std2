from typing import AsyncIterator
from unittest import IsolatedAsyncioTestCase

from ..std2.aitertools import aenumerate, atake, to_async
from ._consts import MODICUM_REP_FACTOR, SMOL_REP_FACTOR


class ToAsync(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        ait: AsyncIterator[int] = to_async([])
        l2 = [i async for i in ait]
        self.assertEqual(l2, [])

    async def test_2(self) -> None:
        l1 = [*range(MODICUM_REP_FACTOR)]
        ait = to_async(iter(l1))
        l2 = [i async for i in ait]
        self.assertEqual(l2, l1)


class AEnum(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        for j in range(SMOL_REP_FACTOR):
            i1 = to_async(enumerate(range(MODICUM_REP_FACTOR), start=j))
            i2 = aenumerate(to_async(range(MODICUM_REP_FACTOR)), start=j)
            l1 = [i async for i in i1]
            l2 = [i async for i in i2]
            self.assertEqual(l2, l1)


class ATake(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        ait = to_async(range(10))
        l2 = [i async for i in atake(ait, 3)]
        self.assertEqual(len(l2), 3)

    async def test_2(self) -> None:
        ait = to_async(range(1))
        l2 = [i async for i in atake(ait, 3)]
        self.assertEqual(len(l2), 1)
