from abc import abstractmethod
from collections.abc import ByteString
from typing import Any, Callable, Final, Iterable, NoReturn, Protocol, TypeVar, Union

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)


CallableT = TypeVar("CallableT", bound=Callable)


class AnyFun(Protocol[_T_co]):
    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> _T_co:
        ...


class AnyAFun(Protocol[_T_co]):
    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> _T_co:
        ...


def never(val: NoReturn) -> NoReturn:
    assert False, type(val).__name__


def is_iterable(val: Any) -> bool:
    """
    Excludes str, bytes, bytearray
    """

    return isinstance(val, Iterable) and not isinstance(val, (str, ByteString))


class VoidType:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return type(self).__name__


Void: Final[VoidType] = VoidType()


def or_else(thing: Union[_T, VoidType], default: _T) -> _T:
    return default if isinstance(thing, VoidType) else thing
