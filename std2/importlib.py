from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from os.path import abspath, basename, splitext
from sys import modules
from types import ModuleType
from typing import Iterator, cast

from .itertools import deiter
from .os.path import segments


def _gen_mod_name(path: str, top_level: str) -> str:
    front, _ = splitext(path)

    def cont() -> Iterator[str]:
        fit = deiter(map(basename, segments(front)))
        tit = deiter(map(basename, segments(top_level)))
        while True:
            f, t = next(fit, None), next(tit, None)
            if f is not None and t is not None and f == t:
                pass
            elif f and not t:
                fit.push_back(f)
                break
            elif t and not f:
                tit.push_back(t)
                break
            else:
                fit.push_back(f)
                tit.push_back(t)
                break

        for _ in tit:
            yield "."
        for f in fit:
            yield "."
            yield f

    return "".join(cont())


def module_from_path(path: str, top_level: str) -> ModuleType:
    abp = abspath(path)
    name = _gen_mod_name(abp, top_level=abspath(top_level))
    spec = spec_from_file_location(name, abp, submodule_search_locations=[])
    mod = module_from_spec(spec)
    modules[mod.__name__] = mod
    cast(Loader, spec.loader).exec_module(mod)
    return mod
