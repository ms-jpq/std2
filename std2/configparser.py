from collections.abc import ByteString, Iterable, MutableMapping
from typing import Any


def hydrate(config: Any) -> Any:
    if isinstance(config, MutableMapping):
        new_config = {}
        for key, val in config.items():
            if isinstance(key, str):
                lhs, _, rhs = key.partition(".")
                if not rhs:
                    new_config[lhs] = val
                else:
                    new_config[lhs] = val
            else:
                new_config[key] = val

        return new_config
    elif isinstance(config, Iterable) and not isinstance(config, (str, ByteString)):
        return tuple(hydrate(el) for el in config)
    else:
        return config
