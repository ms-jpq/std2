from decimal import Decimal
from functools import partial
from itertools import count
from locale import str as format_float
from operator import pow


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
        raise ValueError(f"too big: {size}")
    else:
        for factor, unit in steps:
            product = magnitude * factor
            if product > 1:
                fmt = format_float(round(product, precision))
                return f"{fmt}{unit}"
        else:
            raise ValueError(f"unit overflow: {size}")


def human_readable_size(size: float, precision: int = 3, small: bool = False) -> str:
    if small:
        return _smol(size, precision=precision)
    else:
        return _large(size, precision=precision)

