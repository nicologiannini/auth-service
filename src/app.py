#!/usr/bin/env python
# encoding: utf-8

import os
import handler
from dbengine import database_init
from flask import Flask, request, jsonify
from classes import Response
from utils import log_execution

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

GENERIC_ERROR = 'A generic error occurred on the server.'

'''
NOTE: The service manager sorts the flow for all endpoints by calling the specific 
process handler while catching all significant exceptions.
'''

@log_execution
def service_manager(endpoint_handler):
    response = Response()
    try:
        data = request.get_json()
        endpoint_handler(response, data)
    except AttributeError as error:
        response.failed(400, str(error))
    except ValueError as error:
        response.failed(401, str(error))
    except Exception as e:
        response.failed(500, GENERIC_ERROR)
    return jsonify(response.__dict__), response.status_code


'''
{
    "username": "test",
    "email": "test@gmail.com",
    "password": "12345678",
    "multi_factor": true
}
'''
@app.route('/register/', methods=['POST'])
def register():
    return service_manager(handler.register_handler)


'''
{
    "username": "test",
    "password": "12345678"
}
'''
@app.route('/login/', methods=['POST'])
def access():
    return service_manager(handler.login_handler)


'''
{
    "username": "test",
    "token": "123456"
}
'''
@app.route('/multi_factor/', methods=['POST'])
def multi_factor():
    return service_manager(handler.multi_factor_handler)


if __name__ == '__main__':
    database_init()
    app.run(host='0.0.0.0', port=105)
