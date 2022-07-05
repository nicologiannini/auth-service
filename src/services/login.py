import src.utils.authenticator as authenticator
import src.utils.authorizer as authorizer
import src.utils.exceptions as exceptions
import src.utils.messages as messages
import src.entities.users as users
from src.services.handler import ServiceHandler
from flask import Request


class LoginHandler(ServiceHandler):
    def __init__(self, request: Request):
        super().__init__(request)

    def validate_request(self):
        if not self.request.json or not{
                "email", "password"} == dict(
                self.request.json).keys():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def get_request_data(self):
        data = dict(self.request.json)
        email, password = data["email"], data["password"]
        return email, password

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
