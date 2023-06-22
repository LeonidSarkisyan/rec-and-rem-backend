from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Role(BaseModel):
    name: str
    description: str


class RoleCreate(Role):
    pass
