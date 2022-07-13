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

    def validate_request(self):
        if not set(self.required_key) == dict(self.data).keys():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def get_request_data(self):
        data = dict(self.data)
        values = [data.get(key) for key in self.required_key]
        return (*values,)

    def process(self):
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
