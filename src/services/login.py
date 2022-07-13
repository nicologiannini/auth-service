import src.utils.authenticator as authenticator
import src.utils.authorizer as authorizer
import src.utils.exceptions as exceptions
import src.utils.messages as messages
import src.entities.users as users
from src.services.base import BaseService
from flask import Request


class LoginService(BaseService):
    def __init__(self, request: Request):
        super().__init__(request)
        self.required_key = ("email", "password")

    def validate_request(self) -> None:
        if not self.has_required_data():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def process(self) -> None:
        self.validate_request()
        email, password = self.get_request_data()
        user = users.get_user_by_email(email)
        authenticator.verify_password(user.password, password)
        token = authorizer.generate_token(user.id)

        self.result.build(200, dict(
            message=messages.LOGIN,
            token=token
        ))
