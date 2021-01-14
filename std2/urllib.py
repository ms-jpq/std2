from http.client import HTTPResponse
from typing import Union, cast
from urllib.request import Request, build_opener


def urlopen(req: Union[Request, str]) -> HTTPResponse:
    opener = build_opener()
    resp = opener.open(req)
    return cast(HTTPResponse, resp)
