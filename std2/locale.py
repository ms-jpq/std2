from decimal import Decimal
from functools import partial
from itertools import count
from locale import str as format_float
from operator import pow
from typing import Any, cast


def _large(size: float, precision: int) -> str:
    units = ("", "K", "M", "G", "T", "P", "E", "Z", "Y")
    steps = zip(map(partial(pow, 10), count(0, step=3)), units)

    magnitude = abs(size)
    for factor, unit in steps:
        divided = magnitude / factor
        if divided < 1000:
            fmt = format_float(round(divided, precision))
            return f"{fmt}{unit}"
    else:
        raise ValueError(f"unit overflow: {size}")


def _smol(size: float, precision: int) -> str:
    units = ("", "m", "u", "n", "p", "f", "a", "z", "y")
    steps = zip(map(partial(pow, 10), count(0, step=3)), units)

    magnitude = Decimal(abs(size))
    if magnitude > 1:
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


def human_readable_size(size: float, precision: int = 3, small: bool = False) -> str:
    if small:
        return _smol(size, precision=precision)
    else:
        return _large(size, precision=precision)

