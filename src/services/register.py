import src.utils.authenticator as authenticator
import src.utils.exceptions as exceptions
import src.utils.messages as messages
from src.entities.users import User
from src.services.base import BaseService
from flask import Request


class RegisterService(BaseService):
    def __init__(self, request: Request):
        super().__init__(request)
        self.required_key = ("first_name", "last_name", "email", "password")

    def validate_request(self) -> None:
        if not self.has_required_data():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def process(self) -> None:
        self.validate_request()
        first_name, last_name, email, password = self.get_request_data()
        authenticator.validate_email(email)
        authenticator.validate_password(password)
        hashed_pwd = authenticator.secure_password(password)

        new_user_data = [first_name, last_name, email, hashed_pwd]
        user = User(**dict(zip(self.required_key, new_user_data)))
        user.insert()

        self.result.build(200, dict(
            message=messages.NEW_USER,
            user=user.id
        ))
