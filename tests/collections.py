from unittest import TestCase

from ..std2.collections import defaultlist


class DefaultList(TestCase):
    # def test_1(self) -> None:
    #     ls = [defaultlist(lambda: ""), []]
    #     for l in ls:
    #         self.assertEqual(len(l), 0)
    #         with self.assertRaises(IndexError):
    #             l[1]
    #         with self.assertRaises(IndexError):
    #             l[-1]
    #
    # def test_2(self) -> None:
    #     ls = [defaultlist(lambda: ""), []]
    #     for l in ls:
    #         l.append("a")
    #         self.assertEqual(len(l), 1)
    #         with self.assertRaises(IndexError):
    #             l[1]
    #         with self.assertRaises(IndexError):
    #             l[-2]
    #         self.assertEqual(l[0], "a")
    #         self.assertEqual(l[-1], "a")
    #         self.assertEqual(l[:], ["a"])
    #
    # def test_3(self) -> None:
    #     ls = [defaultlist(lambda: ""), []]
    #     for l in ls:
    #         l.insert(2, "a")
    #         self.assertEqual(len(l), 1)
    #         with self.assertRaises(IndexError):
    #             l[1]
    #         with self.assertRaises(IndexError):
    #             l[-2]
    #         self.assertEqual(l[0], "a")
    #         self.assertEqual(l[-1], "a")
    #         self.assertEqual(l[:], ["a"])

    def test_4(self) -> None:
        ls = [defaultlist(lambda: ""), []]
        for l in ls:
            l.insert(2, "a")
            l.insert(0, "b")
            self.assertEqual(len(l), 2)
            self.assertEqual(l[:], ["b", "a"])
