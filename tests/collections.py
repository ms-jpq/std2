from unittest import TestCase

from ..std2.collections import defaultlist


class DefaultList(TestCase):
    def test_1(self) -> None:
        l1 = defaultlist(lambda: 0)
        self.assertEqual(len(l1), 0)
        with self.assertRaises(IndexError):
            l1[1]
        with self.assertRaises(IndexError):
            l1[-1]

    def test_2(self) -> None:
        l1 = defaultlist(lambda: 0)
        l1.append(1)
        self.assertEqual(len(l1), 1)
        with self.assertRaises(IndexError):
            l1[1]
        with self.assertRaises(IndexError):
            l1[-2]
        self.assertEqual(l1[0], 1)
        self.assertEqual(l1[-1], 1)

    def test_3(self) -> None:
        l1 = defaultlist(lambda: 0)
        l1.insert(2, 1)
        self.assertEqual(len(l1), 3)
        self.assertEqual(l1[0], 0)
        self.assertEqual(l1[2], 1)
        self.assertEqual(l1[-1], 1)
