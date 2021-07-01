from dataclasses import dataclass
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface
from typing import (
    Any,
    ClassVar,
    Generic,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
from unittest import TestCase
from uuid import UUID, uuid4

from ..std2.pickle import DecodeError, new_decoder, new_encoder

T = TypeVar("T")


class Encode(TestCase):
    def test_1(self) -> None:
        p = new_encoder(Sequence[int])
        thing = p([1, 2, 3])
        self.assertEqual(thing, [1, 2, 3])

    def test_2(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: Sequence[str]
            c: Mapping[str, int]

        p = new_encoder(C)
        thing = p(C(a=1, b=["a", "b"], c={"a": 2}))
        self.assertEqual(thing, {"a": 1, "b": ["a", "b"], "c": {"a": 2}})

    def test_3(self) -> None:
        class C(Enum):
            a = b"a"

        p = new_encoder(C)
        thing = p(C.a)
        self.assertEqual(thing, C.a.name)

    def test_4(self) -> None:
        addr = IPv4Address("1.1.1.1")
        inf = IPv4Interface("1.1.1.1/24")

        pa = new_encoder(IPv4Address)
        pi = new_encoder(IPv4Interface)

        a_addr = pa(addr)
        inf_addr = pi(inf)

        self.assertNotEqual(addr, inf)
        self.assertEqual(a_addr, str(addr))
        self.assertEqual(inf_addr, str(inf))


class Decode(TestCase):
    def test_1(self) -> None:
        p = new_decoder(None)
        thing = p(None)
        self.assertEqual(thing, None)

    def test_2(self) -> None:
        p = new_decoder(None)
        with self.assertRaises(DecodeError):
            p(())

    def test_3(self) -> None:
        p = new_decoder(int)
        thing = p(2)
        self.assertEqual(thing, 2)

    def test_4(self) -> None:
        p = new_decoder(int)
        with self.assertRaises(DecodeError):
            p("a")

    def test_5(self) -> None:
        p = new_decoder(str)
        thing = p("a")
        self.assertEqual(thing, "a")

    def test_6(self) -> None:
        p = new_decoder(Optional[str])
        thing = p("a")
        self.assertEqual(thing, "a")

    def test_7(self) -> None:
        p = new_decoder(Optional[str])
        thing = p(None)
        self.assertEqual(thing, None)

    def test_8(self) -> None:
        p = new_decoder(Union[int, str])
        thing = p(2)
        self.assertEqual(thing, 2)

    def test_9(self) -> None:
        p = new_decoder(Union[int, str])
        thing = p("a")
        self.assertEqual(thing, "a")

    def test_10(self) -> None:
        p = new_decoder(Union[int, str])
        with self.assertRaises(DecodeError):
            p(b"a")

    def test_11(self) -> None:
        p = new_decoder(Tuple[int, str])
        thing = p((1, "a"))
        self.assertEqual(thing, [1, "a"])

    def test_12(self) -> None:
        p = new_decoder(Tuple[int, str])
        with self.assertRaises(DecodeError):
            p(("a",))

    def test_13(self) -> None:
        p = new_decoder(Tuple[int, str])
        with self.assertRaises(DecodeError):
            p(("a", 1))

    def test_14(self) -> None:
        p = new_decoder(Any)
        thing = p(None)
        self.assertEqual(thing, None)

    def test_15(self) -> None:
        p = new_decoder(Tuple[int, ...])
        thing = p([1, 2, 3])
        self.assertEqual(thing, [1, 2, 3])

    def test_16(self) -> None:
        p = new_decoder(Tuple[int, ...])
        with self.assertRaises(DecodeError):
            p((1, "a"))

    def test_17(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder(C)
        thing = p({"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_18(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False
            z: ClassVar[bool] = True

        p = new_decoder(C, strict=False)
        thing = p({"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_19(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder(C, strict=False)
        thing = p({"a": 1, "b": [], "d": "d"})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_20(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder(C, strict=True)
        with self.assertRaises(DecodeError) as e:
            p({"a": 1, "b": [], "d": "d"})
        self.assertEqual(e.exception.extra_keys, {"d"})

    def test_21(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder(C)
        with self.assertRaises(DecodeError) as e:
            p({"a": 1})
        self.assertEqual(e.exception.missing_keys, {"b"})

    def test_22(self) -> None:
        p = new_decoder(UUID)
        uuid = uuid4()
        thing = p(str(uuid))
        self.assertEqual(uuid, thing)

    def test_23(self) -> None:
        class E(Enum):
            a = "b"
            b = "a"

        p = new_decoder(Sequence[E])
        thing = p(("a", "b"))
        self.assertEqual(thing, [E.a, E.b])

    def test_24(self) -> None:
        p = new_decoder(Tuple[Literal[5], Literal[2]])
        thing = p([5, 2])
        self.assertEqual(thing, [5, 2])

    def test_25(self) -> None:
        p = new_decoder(Literal[b"a"])
        with self.assertRaises(DecodeError):
            p("a")

    def test_26(self) -> None:
        @dataclass(frozen=True)
        class C(Generic[T]):
            t: T

        with self.assertRaises(ValueError):
            new_decoder(C[int])

    def test_27(self) -> None:
        p = new_decoder(float)
        a = p(0)
        self.assertEqual(a, 0.0)

    def test_28(self) -> None:
        class E(Enum):
            a = "b"
            b = "a"

        p = new_decoder(Sequence[E])
        with self.assertRaises(DecodeError):
            p(("name", "b"))

    def test_29(self) -> None:
        addr = IPv4Address("1.1.1.1")
        inf = IPv4Interface("1.1.1.1/24")

        pa = new_decoder(IPv4Address)
        pi = new_decoder(IPv4Interface)

        d_addr = pa(str(addr))
        d_inf = pi(str(inf))

        self.assertNotEqual(addr, inf)
        self.assertEqual(d_addr, addr)
        self.assertEqual(d_inf, inf)

