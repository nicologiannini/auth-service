#!/usr/bin/env python
# encoding: utf-8

import handler
from flask import Flask, request, jsonify
from classes import Response

app = Flask(__name__)

def service_manager(flow_handler):
    response = Response()
    try:
        data = request.get_json()
        flow_handler(response, data)
    except AttributeError as error:
        response.status_code = 400
        response.error = str(error)
    except ValueError as error:
        response.status_code = 401
        response.error = str(error)
    except Exception as e:
        response.status_code = 500
        response.error = 'A generic error occurred on the server'
    return jsonify(response.__dict__), response.status_code


'''
{
    "username": "test",
    "email": "test@gmail.com",
    "password": "12345678",
    "multi_factor": false
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
@app.route('/access/', methods=['POST'])
def access():
    return service_manager(handler.access_handler)


'''
{
    "username": "test",
    "token": "123456"
}
'''
@app.route('/token_login/', methods=['POST'])
def token_login():
    return service_manager(handler.token_login_handler)


if __name__ == '__main__':
    app.run(debug=True)
