from unittest import TestCase

from ..std2.pickle import CoderError, decode
from typing import Tuple, Union, Optional


class Pickle(TestCase):
    def test_1(self) -> None:
        thing = decode(None, None)
        self.assertEqual(thing, None)

    def test_2(self) -> None:
        thing = decode(int, 2)
        self.assertEqual(thing, 2)

    def test_3(self) -> None:
        thing = decode(str, "a")
        self.assertEqual(thing, "a")

    def test_4(self) -> None:
        thing = decode(Optional[str], "a")
        self.assertEqual(thing, "a")

    def test_5(self) -> None:
        thing = decode(Union[int, str], 2)
        self.assertEqual(thing, 2)

    def test_6(self) -> None:
        thing = decode(Union[int, str], "a")
        self.assertEqual(thing, "a")

    def test_7(self) -> None:
        with self.assertRaises(CoderError):
            decode(Union[int, str], b"a")

    def test_8(self) -> None:
        thing = decode(Tuple[int, str], (1, "a"))
        self.assertEqual(thing, (1, "a"))
