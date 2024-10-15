import requests
from typing import List, Dict, Any, Literal, Tuple, TypeVar, Union
from http import HTTPStatus


ResponseData = Dict[str, Any] | List[Dict[str, Any]] | Literal[True] | str
ErrorData = str | Dict[str, str] | List[Dict[str, str]] | List[str]
TResponse = Tuple[Dict[str, TypeVar("T") | TypeVar("V")], int]


class Response:
    def __init__(self, status: int = HTTPStatus.OK) -> None:
        self._status = status

    def success(self, data: ResponseData) -> TResponse[Literal[True], ResponseData]:
        return dict(status=True, data=data), self._status

    def failed(self, error: ErrorData = "") -> TResponse[Literal[False], ErrorData]:
        return dict(status=False, message=error), self._status


class Request:
    @staticmethod
    def get(url: str):
        return Request.__handle_request(requests.get, url)

    @staticmethod
    def post(url: str, data: dict):
        return Request.__handle_request(requests.post, url=url, json=data)

    @staticmethod
    def __handle_request(req, *args, **kwargs) -> tuple[bool, Union[dict, str]]:
        try:
            response = req(*args, **kwargs)
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.HTTPError:
            return False, Request.__extract_error(response)  # type: ignore
        except requests.exceptions.RequestException as e:
            return False, str(e)

    @staticmethod
    def __extract_error(response: requests.Response) -> Union[dict, str]:
        try:
            return response.json()  # type: ignore
        except ValueError:
            return str(response.text)
