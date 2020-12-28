from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Sequence, Set, Tuple, Union
from unittest import TestCase

from ..std2.pickle import CoderError, decode, encode


class Encode(TestCase):
    def test_1(self) -> None:
        thing = encode([1, 2, 3])
        self.assertEqual(thing, (1, 2, 3))

    def test_2(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: Set[str]

        thing = encode(C(a=1, b=["a", "b"]))
        self.assertEqual(thing, {"a": 1, "b": ("a", "b")})

    def test_3(self) -> None:
        class C(Enum):
            a = b"a"

        thing = encode(C.a)
        self.assertEqual(thing, b"a")


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

    def test_10(self) -> None:
        thing: Tuple[int, ...] = decode(Tuple[int, ...], [1, 2, 3, 4, 5])
        self.assertEqual(thing, (1, 2, 3, 4, 5))
