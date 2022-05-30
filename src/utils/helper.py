import os
import dbengine
import random
from datetime import datetime, timedelta
from classes import User

ENABLE_LOG = os.environ.get('ENABLE_LOG')
DT_FORMAT = '%d/%m/%Y %H:%M:%S'

def retrieve_user(username) -> User:
    raw_user = dbengine.get_user_by_username(username)
    if not raw_user:
        raise ValueError('User not found')
    return User(*list(raw_user)[1:])

def refresh_token(user: User):
    new_token = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    new_token_exp = (
        datetime.now() + timedelta(minutes=5)).strftime(DT_FORMAT)
    user.token = new_token
    user.token_exp = new_token_exp
    if not dbengine.update_user_token_info(user):
        raise Exception

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

def log_detail(message):
    if(ENABLE_LOG):
        now_string = time_now()
        print(f'{now_string} - {message}')
