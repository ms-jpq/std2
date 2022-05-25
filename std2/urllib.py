from http.client import HTTPResponse
from pathlib import PurePosixPath
from typing import Optional, Union, cast
from urllib.parse import unquote as _unquote
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

_OPENER = build_opener()


def urlopen(
    req: Union[Request, str],
    data: Optional[bytes] = None,
    timeout: Optional[float] = None,
) -> HTTPResponse:
    resp = _OPENER.open(req, data=data, timeout=timeout)
    return cast(HTTPResponse, resp)


def uri_path(uri: str, unquote: bool = False) -> PurePosixPath:
    raw = urlsplit(uri).path
    path = _unquote(raw) if unquote else raw
    return PurePosixPath(path)
