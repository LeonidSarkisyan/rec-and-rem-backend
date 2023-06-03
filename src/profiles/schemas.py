from typing import Optional

from pydantic import BaseModel, create_model

from src.schemas import make_optional


class ProfileBase(BaseModel):
    first_name: str
    second_name: str
    username: str


class ProfileCreate(ProfileBase):
    pass


ProfileUpdate = make_optional(ProfileBase)
