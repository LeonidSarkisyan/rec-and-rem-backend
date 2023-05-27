from pydantic import BaseModel


class ProfileBase(BaseModel):
    first_name: str
    second_name: str
    username: str


class ProfileCreate(ProfileBase):
    pass
