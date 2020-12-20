from ..std2.itertools import deiter


from unittest import TestCase


class DoubleEndedIterator(TestCase):
    def test_1(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        d1 = deiter(t1)
        t2 = tuple(d1)
        self.assertEqual(t1, t2)

    def test_2(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        d1 = deiter(())
        d1.push_back(1, 2, 3, 4, 5)
        t2 = tuple(d1)
        self.assertEqual(t1, t2)

    def test_3(self) -> None:
        t1 = (1, 2, 3, 4, 5)
        d1 = deiter((3, 4, 5))
        d1.push_back(1, 2)
        t2 = tuple(d1)
        self.assertEqual(t1, t2)
