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

    def validate_request(self):
        if not set(self.required_key) == dict(self.data).keys():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def get_request_data(self):
        data = dict(self.data)
        values = [data.get(key) for key in self.required_key]   
        return (*values,)

    def process(self):
        self.validate_request()
        email, password = self.get_request_data()
        user = users.get_user_by_email(email)
        authenticator.verify_password(user.password, password)
        token = authorizer.generate_token(user.id)

        self.result.build(200, dict(
            message=messages.LOGIN,
            token=token
        ))
