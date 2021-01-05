from abc import abstractmethod
from typing import Any, Final, NoReturn, Protocol, TypeVar, Union, cast

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


def never() -> NoReturn:
    assert False


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
