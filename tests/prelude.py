from unittest import TestCase

from ..std2 import clamp


class Clamp(TestCase):
    def test_1(self) -> None:
        a = clamp(1, 12, 2)
        self.assertEqual(a, 2)

    def test_2(self) -> None:
        a = clamp(1, 3, 5)
        self.assertEqual(a, 3)

    def test_3(self) -> None:
        a = clamp(1, -5, 2)
        self.assertEqual(a, 1)

    def test_4(self) -> None:
        a = clamp(1.0, -5, 2.0)
        self.assertEqual(a, 1.0)
