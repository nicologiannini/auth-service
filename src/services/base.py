from flask import Request
from src.utils.helper import Result


class BaseService:
    required_key: list

    def __init__(self, request: Request):
        self.request = request
        self.data = request.get_json()
        self.result = Result()

    def validate_request(self):
        raise NotImplementedError

    def has_cookies(self) -> bool:
        return len(self.request.cookies) > 0

    def has_required_data(self) -> bool:
        return set(self.required_key) == dict(self.data).keys()

    def get_request_data(self) -> tuple:
        data = dict(self.data)
        values = [data.get(key) for key in self.required_key]
        return (*values,)

    def get_cookie(self, cookie: str):
        return self.request.cookies.get(cookie)

    def process(self) -> None:
        raise NotImplementedError
