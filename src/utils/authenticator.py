import re
import hashlib
import uuid
import entities.users as users
import utils.exceptions as exceptions
import utils.messages as messages


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not isinstance(
            email, str) or not re.fullmatch(
            regex, email) and len(email):
        raise exceptions.ValidationError(messages.EMAIL_VAL_ERR)

    if users.check_user_by_email(email):
        raise exceptions.ValidationError(messages.EMAIL_ALREADY_EXIST)


def validate_password(password):
    if not 8 <= len(password) <= 16:
        raise exceptions.ValidationError(messages.PASSWORD_ALREADY_EXIST)


def secure_password(password) -> str:
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(
        f'{password}{salt}'.encode('utf-8')).hexdigest()

    return f'{salt}:{hashed_password}'


def verify_password(hashed_password: str, password_to_verify):
    salt, password = hashed_password.split(':')
    if not password == hashlib.sha256(
            f'{password_to_verify}{salt}'.encode('utf-8')).hexdigest():
        raise exceptions.Unauthorized(messages.WRONG_PASSWORD)
