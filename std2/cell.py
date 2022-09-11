from dataclasses import dataclass
from typing import Generic, TypeVar

_T = TypeVar("_T")


@dataclass
class RefCell(Generic[_T]):
    val: _T
