from typing import Iterable, Sequence


def parts(dns: str, sep=".") -> Sequence[str]:
    return dns.split(sep)


def parents(dns: str, sep=".") -> Iterable[str]:
    _, _, rhs = dns.partition(sep)
    if rhs:
        yield rhs
        yield from parents(rhs)
