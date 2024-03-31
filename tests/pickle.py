from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface
from pathlib import PurePath
from typing import (
    AbstractSet,
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

from ..std2.pickle.coders import (
    internet_date_decoder,
    internet_date_encoder,
    iso_date_decoder,
    iso_date_encoder,
    unix_date_decoder,
    unix_date_encoder,
)
from ..std2.pickle.decoder import new_decoder
from ..std2.pickle.encoder import new_encoder
from ..std2.pickle.types import DecodeError

T = TypeVar("T")


class Encode(TestCase):
    def test_1(self) -> None:
        p = new_encoder[Sequence[int]](Sequence[int])
        thing = p([1, 2, 3])
        self.assertEqual(thing, [1, 2, 3])

    def test_2(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: Sequence[str]
            c: Mapping[str, int]

        p = new_encoder[C](C)
        thing = p(C(a=1, b=["a", "b"], c={"a": 2}))
        self.assertEqual(thing, {"a": 1, "b": ["a", "b"], "c": {"a": 2}})

    def test_3(self) -> None:
        class C(Enum):
            a = b"a"

        p = new_encoder[C](C)
        thing = p(C.a)
        self.assertEqual(thing, C.a.name)

    def test_4(self) -> None:
        addr = IPv4Address("1.1.1.1")
        inf = IPv4Interface("1.1.1.1/24")

        pa = new_encoder[IPv4Address](IPv4Address)
        pi = new_encoder[IPv4Interface](IPv4Interface)

        a_addr = pa(addr)
        inf_addr = pi(inf)

        self.assertNotEqual(addr, inf)
        self.assertEqual(a_addr, str(addr))
        self.assertEqual(inf_addr, str(inf))

    def test_5(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: Sequence[str]
            c: Mapping[str, int]

        p = new_encoder[Sequence[C]](Sequence[C])
        thing = p((C(a=1, b=["a", "b"], c={"a": 2}),) * 2)
        self.assertEqual(thing, [{"a": 1, "b": ["a", "b"], "c": {"a": 2}}] * 2)

    def test_6(self) -> None:
        @dataclass(frozen=True)
        class A:
            c: int

        @dataclass(frozen=True)
        class C:
            a: A

        p = new_encoder[C](C)
        thing = p(C(a=A(c=2)))
        self.assertEqual(thing, {"a": {"c": 2}})


class Decode(TestCase):
    def test_1(self) -> None:
        p = new_decoder[None](None)
        thing = p(None)
        self.assertEqual(thing, None)

    def test_2(self) -> None:
        p = new_decoder[None](None)
        with self.assertRaises(DecodeError):
            p(())

    def test_3(self) -> None:
        p = new_decoder[int](int)
        thing = p(2)
        self.assertEqual(thing, 2)

    def test_4(self) -> None:
        p = new_decoder[int](int)
        with self.assertRaises(DecodeError):
            p("a")

    def test_5(self) -> None:
        p = new_decoder[str](str)
        thing = p("a")
        self.assertEqual(thing, "a")

    def test_6(self) -> None:
        p = new_decoder[Optional[str]](Optional[str])
        thing = p("a")
        self.assertEqual(thing, "a")

    def test_7(self) -> None:
        p = new_decoder[Optional[str]](Optional[str])
        thing = p(None)
        self.assertEqual(thing, None)

    def test_8(self) -> None:
        p = new_decoder[Union[int, str]](Union[int, str])
        thing = p(2)
        self.assertEqual(thing, 2)

    def test_9(self) -> None:
        p = new_decoder[Union[int, str]](Union[int, str])
        thing = p("a")
        self.assertEqual(thing, "a")

    def test_10(self) -> None:
        p = new_decoder[Union[int, str]](Union[int, str])
        with self.assertRaises(DecodeError):
            p(b"a")

    def test_11(self) -> None:
        p = new_decoder[Tuple[int, str]](Tuple[int, str])
        thing = p((1, "a"))
        self.assertEqual(thing, [1, "a"])

    def test_12(self) -> None:
        p = new_decoder[Tuple[int, str]](Tuple[int, str])
        with self.assertRaises(DecodeError):
            p(("a",))

    def test_13(self) -> None:
        p = new_decoder[Tuple[int, str]](Tuple[int, str])
        with self.assertRaises(DecodeError):
            p(("a", 1))

    def test_14(self) -> None:
        p = new_decoder[Any](Any)
        thing = p(None)
        self.assertEqual(thing, None)

    def test_15(self) -> None:
        p = new_decoder[Tuple[int, ...]](Tuple[int, ...])
        thing = p([1, 2, 3])
        self.assertEqual(thing, [1, 2, 3])

    def test_16(self) -> None:
        p = new_decoder[Tuple[int, ...]](Tuple[int, ...])
        with self.assertRaises(DecodeError):
            p((1, "a"))

    def test_17(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder[C](C)
        thing = p({"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_18(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False
            z: ClassVar[bool] = True

        p = new_decoder[C](C, strict=False)
        thing = p({"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_19(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder[C](C, strict=False)
        thing = p({"a": 1, "b": [], "d": "d"})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_20(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder[C](C, strict=True)
        with self.assertRaises(DecodeError) as e:
            p({"a": 1, "b": [], "d": "d"})
        self.assertEqual(e.exception.extra_keys, {"d"})

    def test_21(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        p = new_decoder[C](C)
        with self.assertRaises(DecodeError) as e:
            p({"a": 1})
        self.assertEqual(e.exception.missing_keys, {"b"})

    def test_22(self) -> None:
        p = new_decoder[UUID](UUID)
        uuid = uuid4()
        thing = p(str(uuid))
        self.assertEqual(uuid, thing)

    def test_23(self) -> None:
        class E(Enum):
            a = "b"
            b = "a"

        p = new_decoder[Sequence[E]](Sequence[E])
        thing = p(("a", "b"))
        self.assertEqual(thing, [E.a, E.b])

    def test_24(self) -> None:
        p = new_decoder[Tuple[Literal[5], Literal[2]]](Tuple[Literal[5], Literal[2]])
        thing = p([5, 2])
        self.assertEqual(thing, [5, 2])

    def test_25(self) -> None:
        p = new_decoder[Literal[b"a"]](Literal[b"a"])
        with self.assertRaises(DecodeError):
            p("a")

    def test_26(self) -> None:
        @dataclass(frozen=True)
        class C(Generic[T]):
            t: T

        with self.assertRaises(ValueError):
            new_decoder[C[int]](C[int])

    def test_27(self) -> None:
        p = new_decoder[float](float)
        a = p(0)
        self.assertEqual(a, 0.0)

    def test_28(self) -> None:
        class E(Enum):
            a = "b"
            b = "a"

        p = new_decoder[Sequence[E]](Sequence[E])
        with self.assertRaises(DecodeError):
            p(("name", "b"))

    def test_29(self) -> None:
        @dataclass(frozen=True)
        class A:
            a: int

        @dataclass(frozen=True)
        class B(A):
            a: int = 0

        p = new_decoder[B](B)
        b = p({})
        self.assertEqual(b, B())


class Coders(TestCase):
    def test_1(self) -> None:
        addr = IPv4Address("1.1.1.1")
        inf = IPv4Interface("1.1.1.1/24")

        pa = new_decoder[IPv4Address](IPv4Address)
        pi = new_decoder[IPv4Interface](IPv4Interface)

        d_addr = pa(str(addr))
        d_inf = pi(str(inf))

        self.assertNotEqual(addr, inf)
        self.assertEqual(d_addr, addr)
        self.assertEqual(d_inf, inf)

    def test_2(self) -> None:
        p = new_decoder[AbstractSet[str]](AbstractSet[str])
        thing = p(["1", "2"])
        self.assertEqual(thing, {"1", "2"})

    def test_3(self) -> None:
        p = new_decoder[Optional[PurePath]](Optional[PurePath])
        thing = p(None)
        self.assertEqual(thing, None)

    def test_4(self) -> None:
        p = new_decoder[Optional[PurePath]](Optional[PurePath])
        thing = p(".")
        self.assertEqual(thing, PurePath())

    def test_5(self) -> None:
        p = new_decoder[datetime](datetime, decoders=(unix_date_decoder,))
        thing = p(0)
        self.assertEqual(thing, datetime.fromtimestamp(0, tz=timezone.utc))

    def test_6(self) -> None:
        p1 = new_encoder[datetime](datetime, encoders=(unix_date_encoder,))
        p2 = new_decoder[datetime](datetime, decoders=(unix_date_decoder,))
        t0 = datetime.fromtimestamp(0)
        t1 = p1(t0)
        t2 = p2(t1)
        self.assertEqual(t2, t0.replace(tzinfo=timezone.utc))

    def test_7(self) -> None:
        p1 = new_encoder[datetime](datetime, encoders=(iso_date_encoder,))
        p2 = new_decoder[datetime](datetime, decoders=(iso_date_decoder,))
        t0 = datetime.fromtimestamp(0)
        t1 = p1(t0)
        t2 = p2(t1)
        self.assertEqual(t2, t0.replace(tzinfo=timezone.utc))

    def test_8(self) -> None:
        p1 = new_encoder[datetime](datetime, encoders=(internet_date_encoder,))
        p2 = new_decoder[datetime](datetime, decoders=(internet_date_decoder,))
        t0 = datetime.fromtimestamp(0)
        t1 = p1(t0)
        t2 = p2(t1)
        self.assertEqual(t2, t0.replace(tzinfo=timezone.utc))
