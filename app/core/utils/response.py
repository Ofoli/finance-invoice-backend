
from typing import List, Dict, Any, Literal, Tuple, TypeVar
from http import HTTPStatus

ResponseData = Dict[str, Any] | List[Dict[str, Any]]
ErrorData = str | Dict[str, str] | List[Dict[str, str]] | List[str]
TResponse = Tuple[Dict[str, TypeVar("T") | TypeVar("V")], int]


class Response:
    def __init__(self, status: int = HTTPStatus.OK) -> None:
        self._status = status

    def success(self, data: ResponseData) -> TResponse[Literal[True], ResponseData]:
        return dict(status=True, data=data), self._status

    def failed(self, error: ErrorData = "") -> TResponse[Literal[False], ErrorData]:
        return dict(status=False, message=error), self._status
