from os.path import join
from unittest import TestCase

from ..std2.importlib import module_from_path
from ._consts import TOP_LEVEL


class ModFromPath(TestCase):
    def test_1(self) -> None:
        setup_py = join(TOP_LEVEL, "setup.py")
        mod = module_from_path(setup_py, top_level=TOP_LEVEL)
        self.assertEqual(mod.__name__, ".setup")
