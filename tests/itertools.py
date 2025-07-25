from collections.abc import Mapping, Sequence
from unittest import TestCase

from ..std2.itertools import batched_into, deiter, intervals, merged


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


class Merged(TestCase):
    def test_1(self) -> None:
        cases: Mapping[Sequence[int], Sequence[int]] = {
            (): (),
            (1,): [1],
            (1, 2): [1, 2],
            (1, 1): [2],
            (1, 1, 1): [2, 1],
            (1, 1, 2): [4],
            (1, 1, 2, 4): [8],
            (1, 1, 2, 4, 1): [8, 1],
            (1, 1, 2, 1, 1): [4, 2],
            (1, 1, 2, 1, 1, 2, 4): [4, 8],
            (1, 2, 2, 1, 1, 3, 4, 2, 2): [1, 4, 2, 3, 4, 4],
            (2, 2, 2, 2): [4, 4],
            (1, 3, 3, 3, 5, 5): [1, 6, 3, 10],
            (0, 0, 1, 1, 1, 1): [0, 2, 2],
            (5, 5, 5, 3, 3, 7, 7, 7, 7): [10, 5, 6, 14, 14],
            (10, 10, 10, 5, 5, 5, 5): [20, 10, 10, 10],
        }

        for test, expect in cases.items():
            actual = merged(test, merge=lambda a, b: a + b if a == b else None)
            self.assertEqual(actual, expect)
