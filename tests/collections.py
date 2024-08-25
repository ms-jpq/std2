from typing import Sequence
from unittest import TestCase

from ..std2.collections import defaultlist


class DefaultList(TestCase):
    def test_1(self) -> None:
        l2: Sequence[str] = []
        ls = [defaultlist(lambda: ""), []]
        for l1 in ls:
            self.assertEqual(len(l1), 0)
            with self.assertRaises(IndexError):
                l1[1]
            with self.assertRaises(IndexError):
                l1[-1]
            self.assertEqual(l1[:], l2)

    def test_2(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        l2 = ["a"]
        for l1 in ls:
            l1.append("a")
            self.assertEqual(len(l1), 1)
            with self.assertRaises(IndexError):
                l1[1]
            with self.assertRaises(IndexError):
                l1[-2]
            self.assertEqual(l1[0], "a")
            self.assertEqual(l1[-1], "a")
            self.assertEqual(l1[:], l2)

    def test_3(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        l2 = ["a"]
        for l1 in ls:
            l1.insert(2, "a")
            self.assertEqual(len(l1), 1)
            with self.assertRaises(IndexError):
                l1[1]
            with self.assertRaises(IndexError):
                l1[-2]
            self.assertEqual(l1[:], l2)

    def test_4(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        l2 = ["b", "d", "c", "a"]
        for l1 in ls:
            l1.insert(2, "a")
            l1.insert(0, "b")
            l1.insert(-1, "c")
            l1.insert(1, "d")
            self.assertEqual(len(l1), len(l2))
            self.assertEqual(l1[:], l2)
