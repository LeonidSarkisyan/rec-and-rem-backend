from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class UserLogin(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: RoleBase

    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
