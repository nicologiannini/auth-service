#!/usr/bin/env python
# encoding: utf-8

import os
import utils.handler as handler
from dbengine import database_init
from flask import Flask, request, jsonify
from classes import Response
from utils.helper import log_execution

app = Flask(__name__)
app.url_map.strict_slashes = False
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


@app.route('/register/', methods=['POST'])
def register():
    return service_manager(handler.register_handler)


@app.route('/login/', methods=['POST'])
def access():
    return service_manager(handler.login_handler)


@app.route('/login/token/', methods=['POST'])
def multi_factor():
    return service_manager(handler.token_handler)


if __name__ == '__main__':
    database_init()
    app.run(host='0.0.0.0')
