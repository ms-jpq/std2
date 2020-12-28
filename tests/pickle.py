from dataclasses import dataclass
from typing import Any, Optional, Tuple, Union
from unittest import TestCase

from ..std2.pickle import CoderError, decode, encode


class Encode(TestCase):
    def test_1(self) -> None:
        thing = encode({1, 2, 3})
        self.assertEqual(thing, (1, 2, 3))


class Decode(TestCase):
    def test_1(self) -> None:
        thing: None = decode(None, None)
        self.assertEqual(thing, None)

    def test_2(self) -> None:
        thing: int = decode(int, 2)
        self.assertEqual(thing, 2)

    def test_3(self) -> None:
        thing: str = decode(str, "a")
        self.assertEqual(thing, "a")

    def test_4(self) -> None:
        thing: Optional[str] = decode(Optional[str], "a")
        self.assertEqual(thing, "a")

    def test_5(self) -> None:
        thing: int = decode(Union[int, str], 2)
        self.assertEqual(thing, 2)

    def test_6(self) -> None:
        thing: str = decode(Union[int, str], "a")
        self.assertEqual(thing, "a")

    def test_7(self) -> None:
        with self.assertRaises(CoderError):
            decode(Union[int, str], b"a")

    def test_8(self) -> None:
        thing: Tuple[int, str] = decode(Tuple[int, str], (1, "a"))
        self.assertEqual(thing, (1, "a"))

    def test_9(self) -> None:
        thing: None = decode(Any, None)
        self.assertEqual(thing, None)
