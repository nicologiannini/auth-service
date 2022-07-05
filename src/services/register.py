import src.utils.authenticator as authenticator
import src.utils.exceptions as exceptions
import src.utils.messages as messages
import src.entities.users as users
from src.services.handler import ServiceHandler
from flask import Request


class RegisterHandler(ServiceHandler):
    def __init__(self, request: Request):
        super().__init__(request)

    def validate_request(self):
        if not self.request.json or not{
                "first_name", "last_name", "email", "password"} == dict(
                self.request.json).keys():
            raise exceptions.InvalidRequest(messages.INVALID_REQ)

    def get_request_data(self):
        data = dict(self.request.json)
        first_name, last_name, email, password = data["first_name"], data[
            "last_name"], data["email"], data["password"]
        return first_name, last_name, email, password

    def process(self):
        self.validate_request()
        first_name, last_name, email, password = self.get_request_data()
        authenticator.validate_email(email)
        authenticator.validate_password(password)
        hashed_pwd = authenticator.secure_password(password)
        new_user = users.User(first_name=first_name,
                              last_name=last_name,
                              email=email,
                              password=hashed_pwd)
        new_user.insert()
        self.result.build(200, dict(
            message=messages.NEW_USER,
            user=new_user.id
        ))
