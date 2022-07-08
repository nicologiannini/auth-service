import src.utils.authorizer as authorizer
import src.utils.exceptions as exceptions
import src.utils.messages as messages
from src.services.handler import ServiceHandler
from flask import Request


class SessionHandler(ServiceHandler):
    def __init__(self, request: Request):
        super().__init__(request)

    def validate_request(self):
        if not len(self.request.cookies) > 0:
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def get_request_data(self):
        token = self.request.cookies.get(messages.COOKIE_KEY)
        return token

    def process(self):
        self.validate_request()
        token = self.get_request_data()
        payload = authorizer.validate_token(token)

        self.result.build(200, dict(
            message=messages.TOKEN_OK,
            user_id=payload.get("usr")
        ))
