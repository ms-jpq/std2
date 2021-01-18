from typing import Any, MutableMapping, Sequence, Mapping

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
            step = thing.setdefault(head, {})
            _create_element_at(step, val=val, paths=tail)


def hydrate(config: Mapping[str, Any]) -> Mapping[str, Any]:
    new_config: MutableMapping[str, Any] = {}

    def cont(src: Any, dest: Any) -> None:
        if isinstance(src, Mapping):
            for key, val in src.items():
                if isinstance(key, str):
                    paths = key.split(".")
                    _create_element_at(dest, val=val, paths=paths)
                else:
                    dest[key] = val

        elif is_seq(src):
            for el in src:
                hydrate(el)
        else:
            pass

    cont(src=config, dest=new_config)
    return new_config
