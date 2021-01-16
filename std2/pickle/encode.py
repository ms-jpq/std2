from __future__ import annotations

from collections.abc import ByteString
from collections.abc import Iterable as ABC_Iterable
from collections.abc import Mapping as ABC_Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from operator import attrgetter
from typing import Any, Protocol, Sequence, TypeVar

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

        elif isinstance(thing, ABC_Iterable) and not isinstance(
            thing, (str, ByteString)
        ):
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
