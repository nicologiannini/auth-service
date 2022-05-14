#!/usr/bin/env python
# encoding: utf-8

import dbengine
import utils
from flask import Flask, request, jsonify
from classes import User, Response

app = Flask(__name__)

'''
{
    "email": "test@gmail.com",
    "username": "admin",
    "password": "1234",
    "multi_factor": false
}
'''
@app.route('/register/', methods=['POST'])
def register():
    response = Response()
    try:
        registration_data = request.get_json()
        handle_registration(response, registration_data)
    except TypeError as error:
        response.status_code = 400
        response.error = str(error)
    except ValueError as error:
        response.status_code = 401
        response.error = str(error)
    except Exception:
        response.status_code = 500
        response.error = 'A generic error occurred on the server'
    return jsonify(response.__dict__), response.status_code

@app.route('/access/', methods=['GET'])
def access():
    pass

def handle_registration(response: Response, registration_data: dict):
    if(registration_data and {'username', 'email', 'password', 'multi_factor'} <= registration_data.keys()):
        new_user = User()
        new_user.username = utils.validate_username(
            registration_data['username'])
        new_user.email = utils.validate_email(
            registration_data['email'])
        new_user.password = registration_data['password']
        new_user.multi_factor = utils.validate_multi_factor(
            registration_data['multi_factor'])
        if dbengine.insert_user(new_user):
            response.status_code = 200
            response.body = f'{new_user.username} has been created.'
        else:
            raise Exception
    else:
        raise TypeError('Client sent an invalid request.')


if __name__ == '__main__':
    app.run(debug=True)
