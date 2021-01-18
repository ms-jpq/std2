from unittest import TestCase
from ..std2.configparser import hydrate


class Hydrate(TestCase):
    def test_1(self) -> None:
        spec = {"a.b.c": 2}
        config = hydrate(spec)
        expected = {"a": {"b": {"c": 2}}}
        self.assertEqual(config, expected)

    def test_2(self) -> None:
        spec = {"a.b.c": 2, "a": {"b": 4}}
        config = hydrate(spec)
        expected = {"a": {"b": {"c": 2}}}
        self.assertEqual(config, expected)

    def test_3(self) -> None:
        spec = {"a.b.c": 2, "b": 3}
        config = hydrate(spec)
        expected = {"a": {"b": {"c": 2}}, "b": 3}
        self.assertEqual(config, expected)
