import sqlite3

from fastapi import APIRouter

from models.auth_model import Employee, TokenAuth
from models.request_models import BadRequestModel
from settings import settings
from utils.general_utilities import (validate_token_request,
                                     validate_user_request)
from utils.access_token_handler import (check_if_logged_in, decode_access_token,
                                        sign_access_token)
from utils.logger import logger
from utils.sqlite_utils import conn, cursor

router = APIRouter()


@router.post(path="/signup")
async def signup(request: Employee):
    status, message = validate_user_request(request)
    if not status:
        return message
    username, password = request.username, request.password
    is_admin = 1 if request.secret and request.secret == settings.ADMIN_SECRET else 0
    try:
        cursor.execute(
            "INSERT INTO employees(username, password, admin) VALUES (?, ?, ?)",
            (username, password, is_admin),
        )
        conn.commit()
        response = {"is_error": False, "message": "User signed up successfully"}
        logger.success(response)
    except sqlite3.IntegrityError as e:
        response = {"is_error": True, "message": f"User {username} already exists"}
    return response


@router.post(path="/login")
async def login(request: Employee):
    status, message = validate_user_request(request)
    if not status:
        return message
    cursor.execute("SELECT * FROM employees WHERE username=?", (request.username,))
    _id, username, password, is_admin = cursor.fetchone()
    if not (username == request.username and password == request.password):
        return BadRequestModel(message="Invalid username or password.")
    access_token = sign_access_token(username)
    response = {
        "is_error": False,
        "message": "Success",
        "access_token": access_token,
        "is_admin": bool(is_admin)
    }
    logger.success(f"{username} logged in successfully.")
    return response


@router.post("/is_logged_in")
async def is_logged_in(request: TokenAuth):
    status, message = validate_token_request(request)
    if not status:
        return message
    decoded_token = decode_access_token(request.token)
    status = check_if_logged_in(decoded_token)
    return {"status": status}
