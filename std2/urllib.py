from http.client import HTTPResponse
from typing import Union, cast
from urllib.request import Request, build_opener

from .asyncio import run_in_executor


async def urlopen(req: Union[Request, str]) -> HTTPResponse:
    def fetch() -> HTTPResponse:
        opener = build_opener()
        with opener.open(req) as resp:
            return cast(HTTPResponse, resp)

    msg = await run_in_executor(fetch)
    return msg
