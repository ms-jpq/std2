from unittest import TestCase

from ..std2.lex import ParseError, envsubst, split


class Split(TestCase):
    def test_1(self) -> None:
        a = "1\\|2\\\\3|4,5"
        b = tuple(split(a, sep="|", esc="\\"))
        self.assertEqual(b, ("1|2\\3", "4,5"))


class Envsubst(TestCase):
    def test_1(self) -> None:
        a = "${}"
        b = envsubst(a, env={"": ""})
        self.assertEqual(b, "")

    def test_2(self) -> None:
        a = "${a}"
        b = envsubst(a, env={"a": "2"})
        self.assertEqual(b, "2")

    def test_3(self) -> None:
        a = "$$"
        b = envsubst(a, env={})
        self.assertEqual(b, "$")

    def test_4(self) -> None:
        a = "$"
        with self.assertRaises(ParseError):
            envsubst(a, env={})

    def test_5(self) -> None:
        a = "${"
        with self.assertRaises(ParseError):
            envsubst(a, env={})
