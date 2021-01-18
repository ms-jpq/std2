from typing import Iterable, Iterator, Mapping, MutableSequence, TypeVar

T = TypeVar("T")


class ParseError(Exception):
    ...


def escape_with_prefix(stream: Iterable[T], escape: Mapping[T, T]) -> Iterable[T]:
    for unit in stream:
        if unit in escape:
            yield escape[unit]
        yield unit


def escape_with_replacement(stream: Iterable[T], escape: Mapping[T, T]) -> Iterable[T]:
    for unit in stream:
        if unit in escape:
            yield escape[unit]
        else:
            yield unit


def envsubst(text: Iterable[str], env: Mapping[str, str]) -> str:
    def it() -> Iterator[str]:
        it = iter(text)
        for c in it:
            if c == "$":
                nc = next(it, "")
                if nc == "$":
                    yield nc
                elif nc == "{":
                    chars: MutableSequence[str] = []
                    for c in it:
                        if c == "}":
                            name = "".join(chars)
                            if name in env:
                                yield env[name]
                            else:
                                raise ParseError(f"KeyError: expected {name} in env")
                            break
                        else:
                            chars.append(c)
                    else:
                        msg = "Unexpected EOF after ${"
                        raise ParseError(msg, text)
                else:
                    msg = f"Unexpected char: {c} after $, expected $, {{"
                    raise ParseError(msg, text)
            else:
                yield c

    return "".join(it())
