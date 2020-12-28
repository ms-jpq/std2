from unittest import TestCase

from ..std2.pickle import decode


class Pickle(TestCase):
    def test_1(self) -> None:
        n = decode(None, None)
        self.assertEqual(n, None)

    def test_2(self) -> None:
        two = decode(int, 2)
        self.assertEqual(two, 2)

    def test_3(self) -> None:
        a = decode(str, "a")
        self.assertEqual(a, "a")