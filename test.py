#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from os.path import dirname, join, realpath
from unittest import defaultTestLoader
from unittest.runner import TextTestRunner
from unittest.signals import installHandler

_base_ = dirname(realpath(__file__))
_parent_ = dirname(_base_)
_tests_ = join(_base_, "tests")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="count", default=1)
    parser.add_argument("-f", "--fail", action="store_true", default=False)
    parser.add_argument("-b", "--buffer", action="store_true", default=False)
    parser.add_argument("-p", "--pattern", default="*.py")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
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
