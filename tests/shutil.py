from unittest import TestCase

from ..std2.shutil import big_print


class BigPrint(TestCase):
    def test_1(self) -> None:
        big_print("")
