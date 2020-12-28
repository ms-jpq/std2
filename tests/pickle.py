from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Optional, Sequence, Tuple, Union, List
from unittest import TestCase

from ..std2.pickle import DecodeError, decode, encode


class Encode(TestCase):
    def test_1(self) -> None:
        thing = encode([1, 2, 3])
        self.assertEqual(thing, (1, 2, 3))

    def test_2(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: Sequence[str]
            c: Mapping[str, int]

        thing = encode(C(a=1, b=["a", "b"], c={"a": 2}))
        self.assertEqual(thing, {"a": 1, "b": ("a", "b"), "c": {"a": 2}})

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
        with self.assertRaises(DecodeError):
            decode((None), ())

    def test_3(self) -> None:
        thing: int = decode(int, 2)
        self.assertEqual(thing, 2)

    def test_4(self) -> None:
        with self.assertRaises(DecodeError):
            decode(int, "a")

    def test_5(self) -> None:
        thing: str = decode(str, "a")
        self.assertEqual(thing, "a")

    def test_6(self) -> None:
        thing: Optional[str] = decode(Optional[str], "a")
        self.assertEqual(thing, "a")

    def test_7(self) -> None:
        thing: Optional[str] = decode(Optional[str], None)
        self.assertEqual(thing, None)

    def test_8(self) -> None:
        thing: int = decode(Union[int, str], 2)
        self.assertEqual(thing, 2)

    def test_9(self) -> None:
        thing: str = decode(Union[int, str], "a")
        self.assertEqual(thing, "a")

    def test_10(self) -> None:
        with self.assertRaises(DecodeError):
            decode(Union[int, str], b"a")

    def test_11(self) -> None:
        thing: Tuple[int, str] = decode(Tuple[int, str], (1, "a"))
        self.assertEqual(thing, (1, "a"))

    def test_12(self) -> None:
        with self.assertRaises(DecodeError):
            decode(Tuple[int, str], ("a",))

    def test_13(self) -> None:
        with self.assertRaises(DecodeError):
            decode(Tuple[int, str], ("a", 1))

    def test_14(self) -> None:
        thing: None = decode(Any, None)
        self.assertEqual(thing, None)

    def test_15(self) -> None:
        thing: Tuple[int, ...] = decode(Tuple[int, ...], [1, 2, 3])
        self.assertEqual(thing, (1, 2, 3))

    def test_16(self) -> None:
        with self.assertRaises(DecodeError):
            decode(Tuple[int, ...], (1, "a"))

    def test_17(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]

        thing: C = decode(C, {"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[]))
