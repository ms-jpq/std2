from http.client import HTTPResponse
from typing import Optional, Union, cast
from urllib.request import Request, build_opener


def urlopen(req: Union[Request, str], timeout: Optional[float] = None) -> HTTPResponse:
    opener = build_opener()
    resp = opener.open(req, timeout=timeout)
    return cast(HTTPResponse, resp)

