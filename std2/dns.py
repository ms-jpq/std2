from typing import Iterable, MutableSequence, Sequence


def parts(dns: str, sep: str = ".") -> Sequence[str]:
    return dns.split(sep)


def parents(dns: str, sep: str = ".") -> Iterable[str]:
    _, _, rhs = dns.partition(sep)
    if rhs:
        yield rhs
        yield from parents(rhs, sep=sep)


def common_ancestor(dns1: str, dns2: str, sep: str = ".") -> str:
    acc: MutableSequence[str] = []
    for lhs, rhs in zip(reversed(parts(dns1, sep=sep)), reversed(parts(dns2, sep=sep))):
        if lhs == rhs:
            acc.append(lhs)

    return sep.join(reversed(acc))
