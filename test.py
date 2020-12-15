#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from logging import (
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    WARN,
    Formatter,
    StreamHandler,
    getLevelName,
    getLogger,
)
from os.path import dirname, join, realpath
from typing import Iterator, Mapping, Tuple
from unittest import defaultTestLoader
from unittest.runner import TextTestRunner
from unittest.signals import installHandler

_base_ = dirname(realpath(__file__))
_parent_ = dirname(_base_)
_tests_ = join(_base_, "tests", "cases")

_log_fmt_ = """
--  {name}
level:    {levelname}
time:     {asctime}
module:   {module}
line:     {lineno}
function: {funcName}
message:  |-
{message}
"""
_log_date_fmt_ = "%Y-%m-%d %H:%M:%S"


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="count", default=1)
    parser.add_argument("-f", "--fail", action="store_true", default=False)
    parser.add_argument("-b", "--buffer", action="store_true", default=False)
    parser.add_argument("-l", "--log-level", default="INFO")
    parser.add_argument("-p", "--pattern", default="*.py")
    return parser.parse_args()


def gen_lvls() -> Mapping[str, int]:
    def cont() -> Iterator[Tuple[str, int]]:
        for lv in (DEBUG, INFO, WARN, ERROR, FATAL):
            name: str = getLevelName(lv)
            yield name, lv
            yield name.lower(), lv

    return {k: v for k, v in cont()}


def setup_logging(level: str) -> None:
    log = getLogger()
    log.setLevel(gen_lvls().get(level, WARN))

    formatter = Formatter(fmt=_log_fmt_, datefmt=_log_date_fmt_, style="{")
    handlers = (StreamHandler(),)
    for handler in handlers:
        handler.setFormatter(formatter)
        log.addHandler(handler)


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    suite = defaultTestLoader.discover(
        _tests_, top_level_dir=_parent_, pattern=args.pattern
    )
    runner = TextTestRunner(
        verbosity=args.verbosity,
        failfast=args.fail,
        buffer=args.buffer,
    )

    installHandler()
    runner.run(suite)


main()
