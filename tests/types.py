from unittest import TestCase
from ..std2.types import Void, VoidType


class VoidTest(TestCase):
    def test_1(self) -> None:
        self.assertIs(Void, Void)

    def test_2(self) -> None:
        self.assertIsNot(Void, VoidType)

    def test_3(self) -> None:
        self.assertIsNot(Void, VoidType())