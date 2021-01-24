from typing import Mapping
from unittest import TestCase

from ..std2.tree import merge, recur_sort


class Sort(TestCase):
    def test_1(self) -> None:
        a = dict.fromkeys(map(str, range(5, 0, -1)))
        b: Mapping[str, None] = recur_sort(a)
        self.assertNotEqual(tuple(b.items()), tuple(a.items()))
        self.assertEqual(
            tuple(b.items()),
            tuple({"1": None, "2": None, "3": None, "4": None, "5": None}.items()),
        )


class Merge(TestCase):
    def test_1(self) -> None:
        a = merge("a", "b")
        self.assertEqual(a, "b")

    def test_2(self) -> None:
        a = merge({1}, {2})
        self.assertEqual(a, {1, 2})
