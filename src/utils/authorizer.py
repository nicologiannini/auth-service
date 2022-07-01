import jwt
from config import SECRET_KEY
from datetime import datetime


def generate_token(user_id: str, password: str):
    issued_at = int(datetime.timestamp(datetime.now()))
    expires_at = issued_at + (60 * 60 * 12)
    
    payload = {
        "iat": issued_at,
        "exp": expires_at,
        "usr": user_id,
        "pwd": password,
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
