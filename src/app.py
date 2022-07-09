#!/usr/bin/env python
# encoding: utf-8

import os
import src.utils.messages as messages
from src.utils.authorizer import set_session
from src.utils.exceptions import DefaultException
from src.utils.helper import Result
from src.services import BaseService, RegisterService, LoginService, SessionService
from flask import Flask, request, jsonify, make_response, Response
from flask_cors import CORS
from src.engine import database_init

app = Flask(__name__)
app.url_map.strict_slashes = False
app.secret_key = os.environ.get("SECRET_KEY")
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, supports_credentials=True)


def service_manager(service: BaseService) -> Response:
    res = Result()
    try:
        service.process()
        res = service.result
    except DefaultException as err:
        res.failed(err.code, err.message)
    except Exception as e:
        res.failed(500, messages.GENERIC_ERROR)
    response = make_response(jsonify(res.__dict__), res.status_code)
    return response


@app.route("/register/", methods=["POST"])
def register():
    return service_manager(RegisterService(request))


@app.route("/login/", methods=["POST"])
@set_session
def access():
    return service_manager(LoginService(request))


@app.route("/session/", methods=["GET"])
def validate_session():
    return service_manager(SessionService(request))


if __name__ == "__main__":
    database_init()
    app.run(host="127.0.0.1", ssl_context='adhoc')
