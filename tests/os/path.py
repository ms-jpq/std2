from os.path import join
from unittest import TestCase

from ...std2.os.path import ancestors, segments


class Ancestors(TestCase):
    def test_1(self) -> None:
        path = join(*"/abcd")
        a = tuple(ancestors(path))
        self.assertEqual(a, ("/", "/a", "/a/b", "/a/b/c", "/a/b/c/d"))


class Segments(TestCase):
    def test_1(self) -> None:
        path = join(*"/abcd")
        s = tuple(segments(path))
        self.assertEqual(s, ("a", "b", "c", "d"))
