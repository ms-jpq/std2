from abc import abstractmethod
from typing import Any, Final, Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class VoidType:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return type(self).__name__


Void: Final[VoidType] = VoidType()


class AnyFun(Protocol[T_co]):
    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...


class AnyAFun(Protocol[T_co]):
    @abstractmethod
    async def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...
