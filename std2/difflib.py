from difflib import SequenceMatcher
from typing import Iterable, Literal, Sequence, Tuple, TypeVar, cast

from .types import never

T = TypeVar("T")

_OP_CODE = Literal["equal", "delete", "insert", "replace"]


def trans_inplace(
    src: Sequence[T], dest: Sequence[T], unifying: int
) -> Iterable[Tuple[Tuple[int, int], Sequence[T]]]:
    """
    for (lo, hi), replace in inplace_trans(src, dest, n):
      src[lo,hi] = replace
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
                yield (lo, hi), ()
                offset = offset - (i2 - i1)

            elif opcode == "insert":
                yield (lo, hi), dest[j1:j2]
                offset = offset + (j2 - j1)

            elif opcode == "replace":
                yield (lo, hi), dest[j1:j2]
                offset = offset - (i2 - i1) + (j2 - j1)

            else:
                never(opcode)
