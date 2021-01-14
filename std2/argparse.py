from argparse import ArgumentParser
from typing import NoReturn, Optional


class ArgparseError(Exception):
    ...


class ArgParser(ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ArgparseError(message)

    def exit(self, status: int = 0, message: Optional[str] = None) -> NoReturn:
        msg = self.format_help()
        raise ArgparseError(msg)
