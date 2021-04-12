from typing import Iterable, Sequence


def parts(dns: str, sep: str = ".") -> Sequence[str]:
    return dns.split(sep)


def parents(dns: str, sep: str = ".") -> Iterable[str]:
    _, _, rhs = dns.partition(sep)
    if rhs:
        yield rhs
        yield from parents(rhs, sep=sep)
