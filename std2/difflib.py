from difflib import SequenceMatcher
from typing import Hashable, Iterable, Literal, Sequence, Tuple, TypeVar, cast

from .types import never

_H = TypeVar("_H", bound=Hashable)

_OP_CODE = Literal["equal", "delete", "insert", "replace"]


def trans_inplace(
    src: Sequence[_H], dest: Sequence[_H], unifying: int
) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    for (i1, i2), (j1, j2) in trans_inplace(src, dest, n):
      src[i1:i2] = dest[j1:j2]
    """

    matcher = SequenceMatcher(isjunk=None, a=src, b=dest, autojunk=False)
    offset = 0

    for operations in matcher.get_grouped_opcodes(n=unifying):
        for op_name, i1, i2, j1, j2 in operations:
            opcode = cast(_OP_CODE, op_name)
            lo, hi = i1 + offset, i2 + offset

            if opcode == "equal":
                pass

            elif opcode == "delete":
                yield (lo, hi), (j1, j2)
                offset = offset - (i2 - i1)

            elif opcode == "insert":
                yield (lo, hi), (j1, j2)
                offset = offset + (j2 - j1)

            elif opcode == "replace":
                yield (lo, hi), (j1, j2)
                offset = offset - (i2 - i1) + (j2 - j1)

            else:
                never(opcode)
