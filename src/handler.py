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
    # Once the validations are passed and initialized the new user attempts to insert it into the db.
    if(data and {'username', 'email', 'password', 'multi_factor'} <= data.keys()):
        new_user = User()
        new_user.username = utils.validate_username(data['username'])
        new_user.email = utils.validate_email(data['email'])
        new_user.password = utils.validate_password(data['password'])
        new_user.multi_factor = utils.validate_multi_factor(
            data['multi_factor'])
        if dbengine.insert_user(new_user):
            response.status_code = 200
            response.body['message'] = f'{new_user.username} has been created.'
        else:
            raise Exception
    else:
        raise AttributeError(INVALID_REQ)

@utils.log_execution
def login_handler(response: Response, data: dict):
    # Based on the type of authentication decides whether to attempt a direct login or go through token generation.
    def _basic_login(response: Response, user: User, password_to_verify: str):
        utils.verify_password(user.password, password_to_verify)
        session[user.username] = True
        response.status_code = 200
        response.body['message'] = LOGIN_OK

    def _generate_token(response: Response, user: User, password_to_verify: str):
        utils.verify_password(user.password, password_to_verify)
        utils.refresh_token(user)
        sender.send_token_mail(user.email, user.auth_token)
        response.status_code = 200
        response.body['message'] = NEW_TOKEN
        response.body['token'] = user.auth_token

    if(data and {'username', 'password'} <= data.keys()):
        user = User()
        raw_user = utils.retrieve_user(data['username'])
        user.load(*raw_user)
        if not user.multi_factor:
            _basic_login(response, user, data['password'])
        else:
            _generate_token(response, user, data['password'])
    else:
        raise AttributeError(INVALID_REQ)

@utils.log_execution
def multi_factor_handler(response: Response, data: dict):
    # Manage the token verification step and if positive, log in.
    if(data and {'username', 'token'} <= data.keys()):
        user = User()
        raw_user = utils.retrieve_user(data['username'])
        user.load(*raw_user)
        if not user.multi_factor:
            raise ValueError(NOT_ALLOWED)
        utils.verify_token(user.auth_token, user.token_exp_date, data['token'])
        session[user.username] = True
        response.status_code = 200
        response.body['message'] = LOGIN_OK
    else:
        raise AttributeError(INVALID_REQ)
