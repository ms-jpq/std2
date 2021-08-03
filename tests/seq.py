from unittest import TestCase

from ..std2.seq import maybe_indexed


class Indexing(TestCase):
    def test_1(self) -> None:
        seq = (1, 2, 3)
        item = maybe_indexed(seq, at=5, default=None)
        self.assertEqual(item, None)
