from unittest import TestCase

from ..std2.itertools import batched_into, deiter, intervals


class ChunkInto(TestCase):
    def test_1(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        t2 = tuple(batched_into(t1, chunks=2))
        self.assertEqual(t2, ((1, 2, 3), (4, 5)))


class DoubleEndedIterator(TestCase):
    def test_1(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        d1 = deiter(t1)
        t2 = tuple(d1)
        self.assertEqual(t1, t2)

    def test_2(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        d1 = deiter[int](())
        d1.push_back(1, 2, 3, 4, 5)
        t2 = tuple(d1)
        self.assertEqual(t1, t2)

    def test_3(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        d1 = deiter((3, 4, 5))
        d1.push_back(1, 2)
        t2 = tuple(d1)
        self.assertEqual(t1, t2)


class Intervals(TestCase):
    def test_1(self) -> None:
        t1 = (
            range(1, 3),
            range(3, 5),
        )
        t2 = tuple(intervals(t1))
        t3 = (range(1, 5),)
        self.assertEqual(t2, t3)

    def test_2(self) -> None:
        t1 = (
            range(1, 2),
            range(3, 5),
        )
        t2 = tuple(intervals(t1))
        t3 = (
            range(1, 2),
            range(3, 5),
        )
        self.assertEqual(t2, t3)

    def test_3(self) -> None:
        t1 = (
            range(1, 2),
            range(3, 5),
            range(4, 6),
        )
        t2 = tuple(intervals(t1))
        t3 = (
            range(1, 2),
            range(3, 6),
        )
        self.assertEqual(t2, t3)

    def test_4(self) -> None:
        t1 = (
            range(1, 2),
            range(3, 5),
            range(4, 6),
            range(9, 10),
            range(10, 11),
            range(9, 11),
        )
        t2 = tuple(intervals(t1))
        t3 = (
            range(1, 2),
            range(3, 6),
            range(9, 11),
        )
        self.assertEqual(t2, t3)
