from logging import DEBUG, ERROR, FATAL, INFO, WARN, getLevelName
from typing import Iterator, Mapping, Tuple


def _gen_lvls() -> Mapping[str, int]:
    def cont() -> Iterator[Tuple[str, int]]:
        for lv in (DEBUG, INFO, WARN, ERROR, FATAL):
            name: str = getLevelName(lv)
            yield name, lv
            yield name.lower(), lv

    return {k: v for k, v in cont()}


LOG_LEVELS = _gen_lvls()
