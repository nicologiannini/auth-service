import src.utils.authorizer as authorizer
import src.utils.exceptions as exceptions
import src.utils.messages as messages
from src.services.base import BaseService
from flask import Request


class SessionService(BaseService):
    def __init__(self, request: Request):
        super().__init__(request)

    def validate_request(self) -> None:
        if not self.has_cookies():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def process(self) -> None:
        self.validate_request()
        token = self.get_cookie(messages.COOKIE_KEY)
        payload = authorizer.validate_token(token)

        self.result.build(200, dict(
            message=messages.TOKEN_OK,
            user_id=payload.get("usr")
        ))
