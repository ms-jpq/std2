from typing import Any, Mapping, MutableMapping, MutableSequence, Sequence, Tuple

from .types import is_seq


def _create_element_at(
    thing: MutableMapping[str, Any], val: Any, paths: Sequence[str]
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


def hydrate(thing: Any) -> Any:
    if isinstance(thing, Mapping):
        thing2: MutableMapping[str, Any] = {}
        acc: MutableSequence[Tuple[Sequence[str], Any]] = []

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

        for ps, hydrated in acc:
            _create_element_at(thing2, val=hydrated, paths=ps)

        return thing2

    elif is_seq(thing):
        return tuple(map(hydrate, thing))
    else:
        return thing
