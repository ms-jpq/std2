from concurrent.futures import ALL_COMPLETED, Future, wait
from typing import Any, Optional, Sequence


def gather(*futs: Future, timeout: Optional[float] = None) -> Sequence[Any]:
    wait(futs, return_when=ALL_COMPLETED, timeout=timeout)
    return tuple(fut.result() for fut in futs)
