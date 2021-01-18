from unittest import TestCase

from ..std2.tree import merge


class Merge(TestCase):
    def test_1(self) -> None:
        a = merge("a", "b")
        self.assertEqual(a, "b")

    def test_2(self) -> None:
        a = merge({1}, {2})
        self.assertEqual(a, {1, 2})
