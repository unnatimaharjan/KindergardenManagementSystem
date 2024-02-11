from pydantic import BaseModel


class BadRequestModel(BaseModel):
    is_error: bool = True
    status_code: int = 400
    message: str


class EmployeeModel(BaseModel):
    token: str
    full_name: str
    address: str
    phone_number: str
