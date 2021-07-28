from os import environ
from pathlib import Path


def _xdg_path(env: str, *fallback: str) -> Path:
    home = environ.get(env)
    if home:
        return Path(home).resolve()
    else:
        return Path(Path.home(), *fallback).resolve()


def cache_home() -> Path:
    return _xdg_path("XDG_CACHE_HOME", ".cache")


def config_home() -> Path:
    return _xdg_path("XDG_CONFIG_HOME", ".config")


def data_home() -> Path:
    return _xdg_path("XDG_DATA_HOME", ".local", "share")
