from __future__ import annotations

from collections.abc import ByteString
from collections.abc import Iterable as ABC_Iterable
from collections.abc import Mapping as ABC_Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from operator import attrgetter
from typing import Any, Callable, Mapping, Protocol, TypeVar

T = TypeVar("T")


class Encoder(Protocol[T]):
    def __call__(
        self,
        thing: T,
        encoders: Encoders,
    ) -> T:
        ...


Encoders = Mapping[Callable[[Any], bool], Encoder]


def encode(thing: Any, encoders: Encoders = {}) -> Any:
    for predicate, encoder in encoders.items():
        if predicate(thing):
            return encoder(thing, encoders=encoders)
    else:
        if isinstance(thing, ABC_Mapping):
            return {
                encode(k, encoders=encoders): encode(v, encoders=encoders)
                for k, v in thing.items()
            }

        elif isinstance(thing, ABC_Iterable) and not isinstance(
            thing, (str, ByteString)
        ):
            return tuple(thing)

        elif isinstance(thing, Enum):
            return thing.name

        elif is_dataclass(thing):
            return {
                field.name: encode(attrgetter(field.name)(thing), encoders=encoders)
                for field in fields(thing)
            }

        else:
            return thing
