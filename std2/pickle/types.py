from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Mapping as ABC_Mapping
from collections.abc import MutableMapping as ABC_MutableMapping
from collections.abc import MutableSequence as ABC_MutableSequence
from collections.abc import MutableSet as ABC_MutableSet
from collections.abc import Sequence as ABC_Sequence
from collections.abc import Set as ABC_Set
from dataclasses import Field, fields, is_dataclass
from enum import Enum
from inspect import isclass
from locale import strxfrm
from os import linesep
from pprint import pformat
from typing import (
    AbstractSet,
    Any,
    Callable,
    Collection,
    Dict,
    FrozenSet,
    List,
    Literal,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
)

_MAPS_M = {MutableMapping, ABC_MutableMapping, Dict, dict}
MAPS = {Mapping, ABC_Mapping} | _MAPS_M

_SETS_M = {MutableSet, ABC_MutableSet, Set, set}
SETS = {AbstractSet, ABC_Set, FrozenSet, frozenset} | _SETS_M

_SEQS_M = {MutableSequence, ABC_MutableSequence, List, list}
SEQS = {Iterable, Sequence, ABC_Sequence} | _SEQS_M

PRIMITIVES = {bool, int, float, bytes, bytearray, str, type(None)}


def _pprn(thingy: Any) -> str:
    if is_dataclass(thingy):
        fs = sorted(fields(thingy), key=lambda f: strxfrm(f.name))
        listed = ", ".join(map(_pprn, fs))
        return f"key of <{thingy.__qualname__}> :: {{ {listed} }}"
    elif isinstance(thingy, Field):
        return f"{thingy.name}: {thingy.type}"
    elif isclass(thingy) and issubclass(thingy, Enum):
        members = sorted((member.name for member in thingy), key=strxfrm)
        listed = ", ".join(members)
        return f"one of: {{ {listed} }}"
    else:
        return str(thingy)


class _BaseError(Exception):
    def __init__(
        self,
        *args: Any,
        path: Sequence[Any],
        actual: Any,
        missing_keys: Collection[str] = (),
        extra_keys: Collection[str] = (),
    ) -> None:
        super().__init__(*args)
        self.path, self.actual = path, actual
        self.missing_keys, self.extra_keys = missing_keys, extra_keys

    def __str__(self) -> str:
        path = f"{linesep}->{linesep}".join(map(_pprn, self.path))
        missing = ", ".join(sorted(self.missing_keys, key=strxfrm))
        extra = ", ".join(sorted(self.extra_keys, key=strxfrm))
        args = ", ".join(map(str, self.args))
        actual = pformat(self.actual, indent=2)

        l0 = linesep
        l1 = f"Path:{linesep}{path}"
        l2 = f"Actual:{linesep}{actual}"
        l3 = f"Missing Keys: {{{missing}}}"
        l4 = f"Extra Keys:   {{{extra}}}"
        l5 = f"Args:         ({args})"
        return (linesep * 2).join((l0, l1, l2, l3, l4, l5))


class EncodeError(_BaseError):
    ...


class DecodeError(_BaseError):
    ...


EStep = Tuple[Literal[False, True], Union[EncodeError, Any]]
EParser = Callable[[Any], EStep]


class Encoder(Protocol):
    def __call__(
        self, tp: Any, path: Sequence[Any], encoders: Sequence[Encoder]
    ) -> Optional[EParser]:
        ...


DStep = Tuple[Literal[False, True], Union[DecodeError, Any]]
DParser = Callable[[Any], DStep]


class Decoder(Protocol):
    def __call__(
        self, tp: Any, path: Sequence[Any], strict: bool, decoders: Sequence[Decoder]
    ) -> Optional[DParser]:
        ...
