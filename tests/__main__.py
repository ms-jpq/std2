from argparse import ArgumentParser, Namespace
from inspect import getmodulename
from itertools import chain
from os import curdir
from os.path import normcase
from pathlib import Path, PurePath
from sys import exit
from typing import Iterable, Iterator
from unittest import defaultTestLoader
from unittest.case import TestCase
from unittest.runner import TextTestRunner
from unittest.signals import installHandler
from unittest.suite import BaseTestSuite, TestSuite

_TESTS = Path(__file__).resolve(strict=True).parent
_TOP_LV = _TESTS.parent
_ROOT = _TOP_LV.parent


def _tests(suite: BaseTestSuite) -> Iterator[TestCase]:
    for child in suite:
        if isinstance(child, BaseTestSuite):
            yield from _tests(child)
        else:
            yield child


def _names(paths: Iterable[PurePath]) -> Iterator[str]:
    rel = _TESTS.relative_to(_ROOT)
    for path in paths:
        abs = normcase(Path(path).resolve(strict=True))
        name = getmodulename(abs)
        assert name
        mod = curdir.join(chain(rel.parts, (name,)))
        yield mod


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="count", default=1)
    parser.add_argument("-f", "--fail", action="store_true", default=False)
    parser.add_argument("-b", "--buffer", action="store_true", default=False)
    parser.add_argument("paths", type=PurePath, nargs="*", default=())
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    suite = defaultTestLoader.discover(
        normcase(_TESTS), top_level_dir=normcase(_ROOT), pattern="*.py"
    )
    names = {*_names(args.paths)}
    tests = (test for test in _tests(suite) if not names or test.__module__ in names)

    runner = TextTestRunner(
        verbosity=args.verbosity,
        failfast=args.fail,
        buffer=args.buffer,
    )
    installHandler()
    r = runner.run(TestSuite(tests))
    return not r.wasSuccessful()


if __name__ == "__main__":
    exit(main())
