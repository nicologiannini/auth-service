from flask import Request
from src.utils.helper import Result


class ServiceHandler:
    def __init__(self, request: Request):
        self.request = request
        self.data = request.get_json()
        self.result = Result()

    def validate_request(self):
        raise NotImplementedError

    def validate_data(self):
        raise NotImplementedError

    def get_request_data(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError
