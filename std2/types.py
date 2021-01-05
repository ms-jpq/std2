from abc import abstractmethod
from typing import (
    Any,
    Dict,
    Final,
    FrozenSet,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    NoReturn,
    Protocol,
    Sequence,
    Set,
    TypeVar,
    Union,
    cast,
    overload,
)

T = TypeVar("T")
V = TypeVar("V")
T_co = TypeVar("T_co", covariant=True)


def never(value: NoReturn) -> NoReturn:
    assert False, type(value).__name__


@overload
def freeze(coll: Union[Sequence[T], MutableSequence[T], List[T]]) -> Sequence[T]:
    ...


@overload
def freeze(
    coll: Union[Mapping[T, V], MutableMapping[T, V], Dict[T, V]]
) -> Mapping[T, V]:
    ...


@overload
def freeze(coll: Union[FrozenSet[T], MutableSet[T], Set[T]]) -> FrozenSet[T]:
    ...


def freeze(coll: T) -> T:
    return coll


class VoidType:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return type(self).__name__


Void: Final[VoidType] = VoidType()


def or_else(thing: Union[T, VoidType], default: T) -> T:
    return default if thing is Void else cast(T, thing)


class AnyFun(Protocol[T_co]):
    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...


class AnyAFun(Protocol[T_co]):
    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...
