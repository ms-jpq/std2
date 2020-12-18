from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from os import sep
from os.path import basename, relpath, splitext
from sys import modules
from types import ModuleType
from typing import Iterator, cast


def _gen_mod_name(path: str, top_level: str) -> str:
    front, _ = splitext(path)
    base = basename(front)
    rel_name = relpath(front, start=top_level)
    if rel_name == base:
        return f".{rel_name}"
    else:

        def cont() -> Iterator[str]:
            prev = ""
            for c in rel_name:
                if c == sep:
                    if prev == ".":
                        pass
                    else:
                        yield "."
                        prev = "."
                else:
                    yield c
                    prev = c

        return "".join(cont())


def module_from_path(path: str, top_level: str) -> ModuleType:
    name = _gen_mod_name(path, top_level=top_level)
    spec = spec_from_file_location(name, path, submodule_search_locations=[])
    mod = module_from_spec(spec)
    modules[mod.__name__] = mod
    cast(Loader, spec.loader).exec_module(mod)
    return mod
