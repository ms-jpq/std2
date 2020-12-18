from typing import Final


class VoidType:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return type(self).__name__


Void: Final[VoidType] = VoidType()
