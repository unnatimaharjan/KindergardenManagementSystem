from pydantic import BaseModel


class BadRequestModel(BaseModel):
    status_code: int = 400
    message: str
