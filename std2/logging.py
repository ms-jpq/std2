from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    getLevelName,
)
from typing import Iterator, Mapping, Tuple

_LEVELS = (CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING)


def _gen_lvls() -> Mapping[str, int]:
    def cont() -> Iterator[Tuple[str, int]]:
        for lv in _LEVELS:
            name: str = getLevelName(lv)
            yield name, lv
            yield name.lower(), lv

    return {k: v for k, v in cont()}


LOG_LEVELS = _gen_lvls()
