from typing import FrozenSet, Iterator


def sql_escape(param: str, nono: FrozenSet[str], escape: str) -> str:
    def cont() -> Iterator[str]:
        for char in param:
            if char in nono:
                yield escape
            yield char

    return "".join(cont())
