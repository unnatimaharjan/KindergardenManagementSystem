import time
import jwt
from settings import settings


def sign_jwt(username: str) -> str:
    payload = {
        "username": username,
        "expiry": int(time.time() + 3600)
    }
    token = jwt.encode(payload, settings.SECRET, settings.ALGORITHM)
    return token


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.SECRET, settings.ALGORITHM)


def check_if_logged_in(decoded_token: dict) -> bool:
    current_time = int(time.time())
    valid_till = decoded_token["expiry"]
    is_valid = True if current_time < valid_till else False
    return is_valid


def get_user_name(token: str) -> str:
    payload = decode_jwt(token)
    return payload.get("username")
