from unittest import TestCase

from ..std2.tree import merge


class Merge(TestCase):
    def test_1(self) -> None:
        a = merge("a", "b")
        self.assertEqual(a, "b")
