from typing import Iterable, Iterator, Mapping, MutableSequence, TypeVar

_T = TypeVar("_T")


class ParseError(Exception):
    ...


def escape(tokens: Iterable[_T], escape: Mapping[_T, _T]) -> Iterable[_T]:
    for ch in tokens:
        if esc := escape.get(ch):
            yield esc
            yield ch
        else:
            yield ch


def split(tokens: Iterable[str], sep: str, esc: str) -> Iterator[str]:
    acc: MutableSequence[str] = []
    it = iter(tokens)

    for c in it:
        if c == esc:
            nc = next(it, "")
            if nc in {sep, esc}:
                yield nc
            else:
                msg = f"Unexpected char: {nc} after {esc}, expected: {esc} | {sep}"
                raise ParseError(msg)
        elif c == sep:
            yield "".join(acc)
            acc.clear()
        else:
            acc.append(c)

    if acc:
        yield "".join(acc)


def envsubst(tokens: Iterable[str], env: Mapping[str, str]) -> str:
    def cont() -> Iterator[str]:
        it = iter(tokens)
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
                                msg = f"KeyError: expected {name} in env"
                                raise ParseError(msg)
                            break
                        else:
                            chars.append(c)
                    else:
                        msg = "Unexpected EOF after ${"
                        raise ParseError(msg, tokens)
                else:
                    msg = f"Unexpected char: {c} after $, expected $, {{"
                    raise ParseError(msg, tokens)
            else:
                yield c

    return "".join(cont())
