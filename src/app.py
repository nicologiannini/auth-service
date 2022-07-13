#!/usr/bin/env python
# encoding: utf-8

import os
import src.utils.messages as messages
from src.utils.authorizer import set_session
from src.utils.exceptions import DefaultException
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
    try:
        service.process()
    except DefaultException as err:
        service.result.failed(err.code, err.message)
    except Exception as e:
        service.result.failed(500, messages.GENERIC_ERROR)
    finally:
        response = make_response(
            jsonify(service.result.__dict__),
            service.result.status_code)

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
