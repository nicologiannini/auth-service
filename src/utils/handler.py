import src.utils.authenticator as authenticator
import src.utils.exceptions as exceptions
import src.utils.messages as messages
import src.utils.authorizer as authorizer
import src.entities.users as users
from flask import Request
from src.utils.helper import Result


def register_handler(request: Request, result: Result):
    if not request.json or not{
            "first_name", "last_name", "email", "password"} == dict(
            request.json).keys():
        raise exceptions.InvalidRequest(messages.INVALID_REQ)

    data = dict(request.json)
    first_name, last_name, email, password = data["first_name"], data[
        "last_name"], data["email"], data["password"]
    authenticator.validate_email(data["email"])
    authenticator.validate_password(data["password"])
    hashed_pwd = authenticator.secure_password(password)
    user_data = dict(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_pwd
    )
    new_user = users.User(**user_data)
    new_user.insert()

    result.build(200, dict(
        message=messages.NEW_USER,
        user=new_user.id
    ))


def login_handler(request: Request, result: Result):
    if not request.json or not{
            "email", "password"} == dict(
            request.json).keys():
        raise exceptions.InvalidRequest(messages.INVALID_REQ)

    data = dict(request.json)
    email, password = data["email"], data["password"]
    user = users.get_user_by_email(email)
    authenticator.verify_password(user.password, password)

    token = authorizer.generate_token(user.id, password)

    result.build(
        200,
        dict(
            message=messages.LOGIN,
            token=token,
        ))


def validate_session_handler(request: Request, result: Result):
    if not len(request.cookies) > 0:
        raise exceptions.InvalidRequest(messages.INVALID_REQ)

    token = request.cookies.get(messages.COOKIE_KEY)
    payload = authorizer.validate_token(token)

    result.build(200, dict(
        message=messages.TOKEN_OK,
        user_id=payload.get("usr")
    ))
