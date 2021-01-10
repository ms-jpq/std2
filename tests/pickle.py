from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
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

from ..std2.pickle import DecodeError, decode, encode
from ..std2.pickle.coders import (
    datetime_float_decoder,
    datetime_float_encoder,
    datetime_str_decoder,
    datetime_str_encoder,
    uuid_decoder,
    uuid_encoder,
)

T = TypeVar("T")


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
        self.assertEqual(thing, C.a.name)


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
            c: bool = False

        thing: C = decode(C, {"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_18(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False
            z: ClassVar[bool] = True

        thing: C = decode(C, {"a": 1, "b": []})
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_19(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        thing: C = decode(C, {"a": 1, "b": [], "d": "d"}, strict=False)
        self.assertEqual(thing, C(a=1, b=[], c=False))

    def test_20(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        with self.assertRaises(DecodeError) as e:
            decode(C, {"a": 1, "b": [], "d": "d"}, strict=True)
        self.assertEqual(e.exception.extra_keys, ["d"])

    def test_21(self) -> None:
        @dataclass(frozen=True)
        class C:
            a: int
            b: List[str]
            c: bool = False

        with self.assertRaises(DecodeError) as e:
            decode(C, {"a": 1})
        self.assertEqual(e.exception.missing_keys, ["b"])

    def test_22(self) -> None:
        uuid = uuid4()
        thing: UUID = decode(UUID, uuid.hex, decoders=(uuid_decoder,))
        self.assertEqual(uuid, thing)

    def test_23(self) -> None:
        class C(Enum):
            a = "b"
            b = "a"

        thing: Sequence[C] = decode(Sequence[C], ["a", "b"])
        self.assertEqual(thing, (C.a, C.b))

    def test_24(self) -> None:
        thing: Tuple[Literal[5], Literal[2]] = decode(
            Tuple[Literal[5], Literal[2]], [5, 2]
        )
        self.assertEqual(thing, (5, 2))

    def test_25(self) -> None:
        with self.assertRaises(DecodeError):
            decode(Literal[b"a"], "a")

    def test_26(self) -> None:
        @dataclass(frozen=True)
        class C(Generic[T]):
            t: T

        with self.assertRaises(DecodeError):
            decode(C[int], {"t": True})


class RoundTrip(TestCase):
    def test_1(self) -> None:
        before = uuid4()
        thing = encode(before, encoders=(uuid_encoder,))
        after: UUID = decode(UUID, thing, decoders=(uuid_decoder,))
        self.assertEqual(after, before)

    def test_2(self) -> None:
        before = datetime.now(tz=timezone.utc)
        thing = encode(before, encoders=(datetime_str_encoder,))
        after: datetime = decode(datetime, thing, decoders=(datetime_str_decoder,))
        self.assertEqual(after, before)

    def test_3(self) -> None:
        before = datetime.now(tz=timezone.utc)
        thing = encode(before, encoders=(datetime_float_encoder,))
        after: datetime = decode(datetime, thing, decoders=(datetime_float_decoder,))
        self.assertEqual(after, before)
