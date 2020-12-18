from os.path import basename, dirname, join
from unittest import TestCase

from ..std2.importlib import module_from_path
from ._consts import TOP_LEVEL


class ModFromPath(TestCase):
    def test_1(self) -> None:
        setup_py = join(TOP_LEVEL, "setup.py")
        mod = module_from_path(setup_py, top_level=TOP_LEVEL)
        self.assertEqual(mod.__name__, ".setup")

    def test_2(self) -> None:
        setup_py = join(TOP_LEVEL, "setup.py")
        parent = dirname(TOP_LEVEL)
        lower_lv = join(parent, "something", "something")
        mod = module_from_path(setup_py, top_level=lower_lv)
        self.assertEqual(mod.__name__, f"...{basename(TOP_LEVEL)}.setup")
