import time

from models.request_models import BadRequestModel


def validate_user_request(request):
    if not request.username and not request.password:
        return False, BadRequestModel(message="Please enter username and password.")
    if not request.username:
        return False, BadRequestModel(message="Please enter username.")
    if not request.password:
        return False, BadRequestModel(message="Please enter password.")
    return True, None


def validate_token_request(request):
    if not request.token:
        return False, BadRequestModel(message="bad request")
    return True, None


def current_time_in_secs():
    return int(time.time())
