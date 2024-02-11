from pydantic import BaseModel


class Admin(BaseModel):
    username: str
    password: str


class TokenAuth(BaseModel):
    token: str
