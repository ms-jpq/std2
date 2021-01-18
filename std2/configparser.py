from locale import strxfrm
from typing import (Any, Iterable, Mapping, MutableMapping, MutableSequence,
                    Sequence, Tuple)

from .types import is_seq

_Index = Tuple[Sequence[str], Any]


def _create_element_at(
    thing: MutableMapping[str, Any], val: Any, paths: Iterable[str]
) -> None:
    if not isinstance(thing, MutableMapping):
        raise ValueError(thing)
    elif not paths:
        return
    else:
        head, *tail = paths
        if not tail:
            thing[head] = val
        else:
            if not isinstance(thing.get(head), MutableMapping):
                thing[head] = {}
            _create_element_at(thing[head], val=val, paths=tail)


def _sort_keyby(index: _Index) -> Any:
    paths, _ = index
    return tuple(map(strxfrm, paths))


def hydrate(thing: Any) -> Any:
    if isinstance(thing, Mapping):
        thing2: MutableMapping[str, Any] = {}
        acc: MutableSequence[_Index] = []

        for key, val in thing.items():
            hydrated = hydrate(val)

            if isinstance(key, str):
                paths = key.split(".")
                if len(paths) > 1:
                    acc.append((paths, hydrated))
                else:
                    thing2[key] = hydrated
            else:
                thing2[key] = hydrated

        for ps, hydrated in sorted(acc, key=_sort_keyby):
            _create_element_at(thing2, val=hydrated, paths=ps)

        return thing2
    elif is_seq(thing):
        return tuple(map(hydrate, thing))
    else:
        return thing
