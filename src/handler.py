import utils
import sender
import dbengine
from flask import session
from classes import User, Response

INVALID_REQ = 'Client sent an invalid request.'
LOGIN_OK = 'Successful login.'
NEW_TOKEN = 'A new token has been generated.'
NOT_ALLOWED = 'Method not allowed.'

'''
NOTE: Each handler deals with a specific process and cascades all the 
processing needed to complete it.

TODO: Manage login attempts on already logged in users, there should be a /logout/
to refresh session.
'''

@utils.log_execution
def register_handler(response: Response, data: dict):
    if(data and {'username', 'email', 'password', 'multi_factor'} == data.keys()):
        username = utils.validate_username(data['username'])
        email = utils.validate_email(data['email'])
        password = utils.validate_password(data['password'])
        multi_factor = utils.validate_multi_factor(
            data['multi_factor'])
        new_user = User(username, email, password, multi_factor)
        if dbengine.insert_user(new_user):
            response.succeded(200, f'{new_user.username} has been created.')
        else:
            raise Exception
    else:
        raise AttributeError(INVALID_REQ)

@utils.log_execution
def login_handler(response: Response, data: dict):
    def _basic_login(response: Response, user: User, password_to_verify: str):
        utils.verify_password(user.password, password_to_verify)
        session[user.username] = True
        response.succeded(200, LOGIN_OK)

    def _generate_token(response: Response, user: User, password_to_verify: str):
        utils.verify_password(user.password, password_to_verify)
        utils.refresh_token(user)
        sender.send_token_mail(user.email, user.auth_token)
        response.succeded(200, NEW_TOKEN)

    if(data and {'username', 'password'} == data.keys()):
        raw_user = utils.retrieve_user(data['username'])
        user = User(*list(raw_user)[1:])
        if not user.multi_factor:
            _basic_login(response, user, data['password'])
        else:
            _generate_token(response, user, data['password'])
    else:
        raise AttributeError(INVALID_REQ)

@utils.log_execution
def multi_factor_handler(response: Response, data: dict):
    if(data and {'username', 'token'} == data.keys()):
        raw_user = utils.retrieve_user(data['username'])
        user = User(*list(raw_user)[1:])
        if not user.multi_factor:
            raise ValueError(NOT_ALLOWED)
        utils.verify_token(user.auth_token, user.token_exp_date, data['token'])
        session[user.username] = True
        response.succeded(200, LOGIN_OK)
    else:
        raise AttributeError(INVALID_REQ)
