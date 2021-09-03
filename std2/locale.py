from decimal import Decimal
from functools import partial
from itertools import count
from locale import str as format_float
from locale import strxfrm
from operator import pow
from pathlib import PurePath
from typing import Any, Sequence, cast


def path_sort_key(path: PurePath) -> Sequence[str]:
    return tuple(map(strxfrm, path.parts))


def si_prefixed(size: float, precision: int = 3) -> str:
    units = ("", "K", "M", "G", "T", "P", "E", "Z", "Y")
    steps = zip(map(partial(pow, 10), count(0, step=3)), units)

    magnitude = Decimal(abs(size))
    for factor, unit in steps:
        divided = magnitude / factor
        if divided < 1000:
            fmt = format_float(round(divided, precision))
            return f"{fmt}{unit}"
    else:
        raise ValueError(f"unit overflow: {size}")


def si_prefixed_smol(size: float, precision: int = 3) -> str:
    units = ("", "m", "u", "n", "p", "f", "a", "z", "y")
    steps = zip(map(partial(pow, 10), count(0, step=3)), units)

    magnitude = Decimal(abs(size))
    if magnitude == 0 or magnitude > 1:
        return format_float(round(cast(Any, magnitude), precision))
    else:
        for factor, unit in reversed(tuple(steps)):
            product = magnitude * factor
            if product < 1:
                raise ValueError(f"unit underflow: {size}")
            elif product < 1000:
                fmt = format_float(round(product, precision))
                return f"{fmt}{unit}"
        else:
            assert False
