from fastapi import APIRouter

from models.auth_model import Admin, TokenAuth
from models.request_models import BadRequestModel
from utils.general_utilities import validate_user_request, validate_token_request
from utils.sqlite_utils import cursor, conn
from utils.logger import logger
from utils.jwt_handler import sign_jwt, decode_jwt, check_if_logged_in

router = APIRouter()


@router.post(path="/signup")
async def signup(request: Admin):
    status, message = validate_user_request(request)
    if not status:
        return message
    username, password = request.username, request.password
    cursor.execute("INSERT INTO admins(username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    response = {"message": "User signed up successfully"}
    logger.success(response)
    return response


@router.post(path="/login")
async def login(request: Admin):
    status, message = validate_user_request(request)
    if not status:
        return message
    cursor.execute("SELECT * FROM admins WHERE username=?", (request.username,))
    id, username, password = cursor.fetchone()
    if not (username == request.username and password == request.password):
        return BadRequestModel(message="Invalid username or password.")
    access_token = sign_jwt(username)
    response = {
        "message": "success",
        "access_token": access_token
    }
    logger.success(f"{username} loggen in successfully")
    return response


@router.post("/is_logged_in")
async def is_logged_in(request: TokenAuth):
    status, message = validate_token_request(request)
    if not status:
        return message
    decoded_token = decode_jwt(request.token)
    status = check_if_logged_in(decoded_token)
    return {"logged_in": status}
