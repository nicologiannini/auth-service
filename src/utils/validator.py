import re
import dbengine
import hashlib, uuid
from datetime import datetime
from utils.helper import time_now

DT_FORMAT = '%d/%m/%Y %H:%M:%S'

def validate_username(username) -> str:
    if not isinstance(username, str):
        raise TypeError('The username should be type string')
    if not 4 <= len(username) <= 16:
        raise ValueError('This username does not respect requirements')
    if dbengine.get_user_by_username(username):
        raise ValueError('This username is already registered')
    return username

def validate_email(email) -> str:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not isinstance(email, str):
        raise TypeError('The email should be type string')
    if not re.fullmatch(regex, email) and len(email):
        raise ValueError('Apparently this is not an email')
    if dbengine.get_user_by_email(email):
        raise ValueError('This email is already registered')
    return email

def validate_password(password) -> str:
    if not 8 <= len(password) <= 16:
        raise ValueError('This password does not respect requirements')
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(f'{password}{salt}'.encode('utf-8')).hexdigest()
    return f'{salt}:{hashed_password}'

def validate_multi_factor(is_enabled: bool) -> int:
    if not isinstance(is_enabled, bool):
        raise ValueError('multi_factor should be boolean type')
    return 1 if is_enabled else 0

def verify_token(last_token, last_token_exp, token_to_verify):
    last_token_exp = datetime.strptime(last_token_exp, DT_FORMAT)
    if last_token != token_to_verify:
        raise ValueError('Invalid token')
    if datetime.strptime(time_now(), DT_FORMAT) > last_token_exp:
        raise ValueError('This token is expired')
    return True

def verify_password(hashed_password: str, password_to_verify):
    salt, password = hashed_password.split(':')
    if not password == hashlib.sha256(f'{password_to_verify}{salt}'.encode('utf-8')).hexdigest():
        raise ValueError('Wrong password')
    return True
