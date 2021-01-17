from __future__ import annotations

from collections.abc import Mapping as ABC_Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from operator import attrgetter
from typing import Any, Protocol, Sequence, TypeVar

from ..types import is_seq

T_co = TypeVar("T_co", covariant=True)


class EncodeError(Exception):
    ...


class Encoder(Protocol[T_co]):
    def __call__(
        self,
        thing: Any,
        encoders: Encoders,
    ) -> T_co:
        ...


Encoders = Sequence[Encoder[Any]]


def encode(thing: Any, encoders: Encoders = ()) -> Any:
    for encoder in encoders:
        try:
            return encoder(thing, encoders=encoders)
        except EncodeError:
            pass

    else:
        if isinstance(thing, ABC_Mapping):
            return {
                encode(k, encoders=encoders): encode(v, encoders=encoders)
                for k, v in thing.items()
            }

        elif is_seq(thing):
            return tuple(encode(item, encoders=encoders) for item in thing)

        elif isinstance(thing, Enum):
            return thing.name

        elif is_dataclass(thing):
            return {
                field.name: encode(attrgetter(field.name)(thing), encoders=encoders)
                for field in fields(thing)
            }

        else:
            return thing
