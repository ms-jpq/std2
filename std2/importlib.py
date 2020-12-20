from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from itertools import zip_longest
from os.path import abspath, basename, splitext
from sys import modules
from types import ModuleType
from typing import Iterator, cast

from .os.path import ancestors


def _gen_mod_name(path: str, top_level: str) -> str:
    front, _ = splitext(path)

    def cont() -> Iterator[str]:
        for p, t in zip_longest(
            map(basename, ancestors(front)), map(basename, ancestors(top_level))
        ):
            if p == t:
                pass
            elif p and not t:
                yield "."
                yield p
            elif t and not p:
                yield "."
                yield t
            else:
                pass

    return "".join(cont())


def module_from_path(path: str, top_level: str) -> ModuleType:
    abp = abspath(path)
    name = _gen_mod_name(abp, top_level=abspath(top_level))
    spec = spec_from_file_location(name, abp, submodule_search_locations=[])
    mod = module_from_spec(spec)
    modules[mod.__name__] = mod
    cast(Loader, spec.loader).exec_module(mod)
    return mod
