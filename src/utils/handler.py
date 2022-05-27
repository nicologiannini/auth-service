import utils.helper as helper
import utils.validator as validator
import utils.sender as sender
import dbengine
from classes import User, Response

INVALID_REQ = 'Client sent an invalid request.'
LOGIN_OK = 'Successful login.'
NEW_TOKEN = 'A new token has been generated.'
FORBIDDEN = 'Method not allowed.'

'''
NOTE: Each handler deals with a specific process and cascades all the 
processing needed to complete it.

TODO: Manage login attempts on already logged in users, there should be a /logout/
to refresh session.
'''

@helper.log_execution
def register_handler(response: Response, data: dict):
    if(data and {'username', 'email', 'password', 'multi_factor'} == data.keys()):
        username = validator.validate_username(data['username'])
        email = validator.validate_email(data['email'])
        password = validator.validate_password(data['password'])
        multi_factor = validator.validate_multi_factor(
            data['multi_factor'])
        new_user = User(username, email, password, multi_factor)
        if dbengine.insert_user(new_user):
            response.succeded(200, f'{new_user.username} has been created.')
        else:
            raise Exception
    else:
        raise AttributeError(INVALID_REQ)

@helper.log_execution
def login_handler(response: Response, data: dict):
    if(data and {'username', 'password'} == data.keys()):
        user = helper.retrieve_user(data['username'])
        validator.verify_password(user.password, data['password'])
        if not user.multi_factor:
            _basic_login(response, user)
        else:
            _generate_token(response, user)
    else:
        raise AttributeError(INVALID_REQ)

@helper.log_execution
def multi_factor_handler(response: Response, data: dict):
    if(data and {'username', 'token'} == data.keys()):
        user = helper.retrieve_user(data['username'])
        if not user.multi_factor:
            raise ValueError(FORBIDDEN)
        validator.verify_token(
            user.auth_token, user.token_exp_date, data['token'])
        _basic_login(response, user)
    else:
        raise AttributeError(INVALID_REQ)

def _basic_login(response: Response, user: User):
    response.succeded(200, LOGIN_OK)

def _generate_token(response: Response, user: User):
    helper.refresh_token(user)
    sender.send_token_mail(user.email, user.auth_token)
    response.succeded(200, NEW_TOKEN)