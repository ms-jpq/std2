from contextlib import contextmanager
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Logger, getLevelName
from os import linesep
from shutil import get_terminal_size
from typing import Any, Iterator, Mapping, Tuple

_LEVELS = (CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING)


def _gen_lvls() -> Mapping[str, int]:
    def cont() -> Iterator[Tuple[str, int]]:
        for lv in _LEVELS:
            name: str = getLevelName(lv)
            yield name, lv
            yield name.casefold(), lv

    return {k: v for k, v in cont()}


LOG_LEVELS = _gen_lvls()


@contextmanager
def with_tracking(log: Logger, suppress: bool = False) -> Iterator[None]:
    try:
        yield None
    except Exception as e:
        log.exception("%s", e)
        if not suppress:
            raise


def big_print(thing: Any, sep: str = "-") -> str:
    col, _ = get_terminal_size()
    line = sep * col
    msg = f"{line}{linesep}{thing}{linesep}{line}"
    return msg
