import time

import jwt

from settings import settings
from utils.general_utilities import current_time_in_secs


def sign_access_token(username: str) -> str:
    payload = {"username": username, "expiry": current_time_in_secs()}
    token = jwt.encode(payload, settings.SECRET, settings.ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET, settings.ALGORITHM)
    except:
        return {}


def check_if_logged_in(decoded_token: dict) -> bool:
    current_time = int(time.time())
    valid_till = decoded_token["expiry"]
    is_valid = True if current_time < valid_till else False
    return is_valid


def get_user_name(token: str) -> str:
    payload = decode_access_token(token)
    return payload.get("username")
