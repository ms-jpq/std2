from typing import Iterable, Iterator, Mapping, Tuple


def quantiles(data: Iterable[float], *quantiles: int) -> Mapping[int, float]:
    ordered = sorted(data)

    def cont() -> Iterator[Tuple[int, float]]:
        for quantile in quantiles:
            assert quantile >= 0 and quantile <= 100
            if ordered:
                idx = round((len(ordered) - 1) * (quantile / 100))
                yield quantile, ordered[idx]

    return {k: v for k, v in cont()}
