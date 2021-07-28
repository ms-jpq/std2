from http.client import HTTPResponse
from typing import Optional, Union, cast
from urllib.request import Request, build_opener

_OPENER = build_opener()


def urlopen(req: Union[Request, str], timeout: Optional[float] = None) -> HTTPResponse:
    resp = _OPENER.open(req, timeout=timeout)
    return cast(HTTPResponse, resp)
