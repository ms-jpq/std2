from unittest import TestCase

from ..std2.shutil import hr_print


class HR(TestCase):
    def test_1(self) -> None:
        hr_print("")
