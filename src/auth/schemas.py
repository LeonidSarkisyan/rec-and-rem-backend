from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class UserLogin(UserBase):
    password: str
