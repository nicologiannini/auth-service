import jwt
import src.utils.messages as messages
from flask import Response
from src.config import SECRET_KEY
from datetime import datetime


def generate_token(user_id: str) -> str:
    issued_at = int(datetime.timestamp(datetime.now()))
    expires_at = issued_at + (60 * 60 * 12)
    payload = {
        "iat": issued_at,
        "exp": expires_at,
        "usr": user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def validate_token(token) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms="HS256",
        options=dict(
            verify_signature=True,
            verify_iat=True
        )
    )
    return payload


def generate_session_cookie(response: Response) -> Response:
    response_data = dict(response.json)
    if response_data.get("status_code") == 200:
        cookie = dict(
            key=messages.COOKIE_KEY,
            value=response_data.get("body")["token"],
            domain=None,
            secure=True,
            samesite="None",
            httponly=True
        )
        response.set_cookie(**cookie)
        
    return response


def set_session(func):
    def inner():
        response = func()
        generate_session_cookie(response)
        return response

    return inner
