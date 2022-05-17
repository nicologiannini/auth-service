import os
import dbengine
import re
import random
import smtplib
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from classes import User

ENABLE_LOG = os.environ['ENABLE_LOG']
DT_FORMAT = '%d/%m/%Y %H:%M:%S'

def validate_username(username):
    if not isinstance(username, str):
        raise TypeError('The username should be type string')
    if not 4 <= len(username) <= 16:
        raise ValueError('This username does not respect requirements')
    if dbengine.get_user_by_username(username):
        raise ValueError('This username is already registered')
    return username

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not isinstance(email, str):
        raise TypeError('The email should be type string')
    if not re.fullmatch(regex, email) and len(email):
        raise ValueError('Apparently this is not an email')
    if dbengine.get_user_by_email(email):
        raise ValueError('This email is already registered')
    return email

def validate_password(password):
    if not 8 <= len(password) <= 16:
        raise ValueError('This password does not respect requirements')
    return generate_password_hash(password).decode('utf-8')

def validate_multi_factor(is_enabled: bool):
    if not isinstance(is_enabled, bool):
        raise ValueError('multi_factor should be boolean type')
    return 1 if is_enabled else 0

def retrieve_user(username):
    raw_user = dbengine.get_user_by_username(username)
    if not raw_user:
        raise ValueError('User not found')
    return raw_user

def verify_password(hashed_password, password_to_verify):
    if not check_password_hash(hashed_password, password_to_verify):
        raise ValueError('Wrong password')

def refresh_token(user: User):
    new_token = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    new_token_exp_date = (datetime.now() + timedelta(minutes=5)).strftime(DT_FORMAT)
    user.auth_token = new_token
    user.token_exp_date = new_token_exp_date
    if not dbengine.update_user_token_info(user):
        raise Exception
    return True

def verify_token(last_token, last_token_exp_date, token_to_verify):
    last_token_exp_date = datetime.strptime(last_token_exp_date, DT_FORMAT)
    if last_token != token_to_verify:
        raise ValueError('Invalid token')
    if datetime.strptime(time_now(), DT_FORMAT) > last_token_exp_date:
        raise ValueError('This token is expired')
    return True

def send_token_mail(receiver, token):
    try:
        sender = 'noreply@localhost.com'
        smtp_obj = smtplib.SMTP('localhost')
        smtp_obj.sendmail(sender, [receiver], f'Your token: {token}')
    except Exception as e:
        log_detail(f'Token: {token} not sent')

def time_now() -> str:
    now = datetime.now()
    return now.strftime(DT_FORMAT)

def log_execution(function):
    def execution(*args, **kwargs):
        if(ENABLE_LOG):
            now_string = time_now()
            function_name = function.__name__
            print(f'{now_string} - {function_name} has been executed')
        return function(*args, **kwargs)
    return execution

def log_detail(message) -> None:
    if(ENABLE_LOG):
        now_string = time_now()
        print(f'{now_string} - {message}')
