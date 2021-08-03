from abc import abstractmethod
from collections.abc import ByteString, Container
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from typing import Any, Callable, Final, NoReturn, Protocol, TypeVar, Union

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

Real = TypeVar("Real", int, float)

IPAddress = Union[IPv4Address, IPv6Address]
IPNetwork = Union[IPv4Network, IPv6Network]
IPInterface = Union[IPv4Interface, IPv6Interface]


class _SupportsLT(Protocol):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...


SupportsLT = TypeVar("SupportsLT", bound=_SupportsLT)

CallableT = TypeVar("CallableT", bound=Callable)


class AnyFun(Protocol[T_co]):
    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...


class AnyAFun(Protocol[T_co]):
    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...


def never(val: NoReturn) -> NoReturn:
    assert False, type(val).__name__


def is_it(val: Any) -> bool:
    """
    Excludes str, bytes, bytearray
    """

    return isinstance(val, Container) and not isinstance(val, (str, ByteString))


class VoidType:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return type(self).__name__


Void: Final[VoidType] = VoidType()


def or_else(thing: Union[T, VoidType], default: T) -> T:
    return default if isinstance(thing, VoidType) else thing
