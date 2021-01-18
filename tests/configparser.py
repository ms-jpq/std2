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

    def test_4(self) -> None:
        spec = {"a": ({"b.c": 4}, 5)}
        config = hydrate(spec)
        expected = {"a": ({"b": {"c": 4}}, 5)}
        self.assertEqual(config, expected)

    def test_5(self) -> None:
        spec = {"a": ({"b.c": 4}, {"e.f": 5})}
        config = hydrate(spec)
        expected = {"a": ({"b": {"c": 4}}, {"e": {"f": 5}})}
        self.assertEqual(config, expected)

    def test_6(self) -> None:
        spec = {"a.b": 2, "a": 1}
        config = hydrate(spec)
        expected = {"a": {"b": 2}}
        self.assertEqual(config, expected)

    def test_7(self) -> None:
        spec = {"a.b": 2, "a": {}}
        config = hydrate(spec)
        expected = {"a": {"b": 2}}
        self.assertEqual(config, expected)

    def test_8(self) -> None:
        spec = {"a.b.c": 3, "a.b": 2}
        config = hydrate(spec)
        expected = {"a": {"b": {"c": 3}}}
        self.assertEqual(config, expected)
