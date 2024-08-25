from unittest import TestCase

from ..std2.collections import defaultlist


class DefaultList(TestCase):
    def test_1(self) -> None:
        l1 = defaultlist(lambda: "")
        l2 = []
        ls = [l1, []]
        for l in ls:
            self.assertEqual(len(l), 0)
            with self.assertRaises(IndexError):
                l[1]
            with self.assertRaises(IndexError):
                l[-1]
            self.assertEqual(l[:], l2)

    def test_2(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        l2 = ["a"]
        for l in ls:
            l.append("a")
            self.assertEqual(len(l), 1)
            with self.assertRaises(IndexError):
                l[1]
            with self.assertRaises(IndexError):
                l[-2]
            self.assertEqual(l[0], "a")
            self.assertEqual(l[-1], "a")
            self.assertEqual(l[:], l2)

    def test_3(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        l2 = ["a"]
        for l in ls:
            l.insert(2, "a")
            self.assertEqual(len(l), 1)
            with self.assertRaises(IndexError):
                l[1]
            with self.assertRaises(IndexError):
                l[-2]
            self.assertEqual(l[:], l2)

    def test_4(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        l2 = ["b", "c", "a"]
        for l1 in ls:
            l1.insert(2, "a")
            l1.insert(0, "b")
            l1.insert(-1, "c")
            self.assertEqual(len(l1), 3)
            self.assertEqual(l1[:], l2)
