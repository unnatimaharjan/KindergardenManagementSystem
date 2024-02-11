from pydantic import BaseModel


class Employee(BaseModel):
    username: str
    password: str
    secret: str = None


class TokenAuth(BaseModel):
    token: str
