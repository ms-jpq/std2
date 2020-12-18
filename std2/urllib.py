from http.client import HTTPResponse
from typing import Any, Union, cast
from urllib.request import Request, build_opener

from .asyncio import run_in_executor


async def req(req: Union[Request, str]) -> HTTPResponse:
    def _req() -> Any:
        opener = build_opener()
        with opener.open(req) as resp:
            return cast(HTTPResponse, resp)

    msg = await run_in_executor(_req)
    return msg
