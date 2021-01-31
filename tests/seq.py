from asyncio import sleep
from unittest import IsolatedAsyncioTestCase


from ..std2.seq import maybe_indexed


class Indexing(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        seq = (1, 2, 3)
        item = maybe_indexed(seq, at=5)
        self.assertEqual(item, None)
