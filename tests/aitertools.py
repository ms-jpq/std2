from asyncio import sleep
from typing import AsyncIterator
from unittest import IsolatedAsyncioTestCase

from ..std2 import anext
from ..std2.aitertools import aenumerate, atake, merge, to_async
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


class ANext(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        ait: AsyncIterator[int] = to_async([])
        with self.assertRaises(StopAsyncIteration):
            await ait.__anext__()
        with self.assertRaises(StopAsyncIteration):
            await anext(ait)
        two = await anext(ait, 2)
        self.assertEqual(two, 2)

    async def test_2(self) -> None:
        ait = to_async([2])
        two = await anext(ait)
        self.assertEqual(two, 2)


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


class Merge(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        l2 = [i async for i in merge(*(to_async(range(10)) for _ in range(4)))]
        self.assertEqual(len(l2), 40)

    async def test_2(self) -> None:
        cut_off = 5

        async def cont() -> AsyncIterator[int]:
            for i in range(100):
                if i > cut_off + 1:
                    self.fail()

                yield i

        async for n in merge(*(cont() for _ in range(20))):
            if n == cut_off:
                break
        else:
            self.fail()

        for _ in range(1000):
            await sleep(0)

    async def test_3(self) -> None:
        async def cont() -> AsyncIterator[int]:
            for i in range(100):
                if 1 == 1:
                    self.fail()
                else:
                    yield i

        _ = merge(*(cont() for _ in range(20)))
        for _ in range(1000):
            await sleep(0)

    async def test_4(self) -> None:
        async def cont() -> AsyncIterator[int]:
            for i in range(100):
                yield i

        with self.assertRaises(RuntimeError):
            async for n in merge(*(cont() for _ in range(20))):
                if n > 2:
                    raise RuntimeError()

        for _ in range(1000):
            await sleep(0)

    async def test_5(self) -> None:
        async def cont() -> AsyncIterator[int]:
            for i in range(100):
                if i < 5:
                    yield i
                else:
                    raise RuntimeError()

        with self.assertRaises(RuntimeError):
            async for _ in merge(*(cont() for _ in range(20))):
                pass

        for _ in range(1000):
            await sleep(0)
