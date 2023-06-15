from typing import List

from pydantic import BaseModel

from src.abstract.schemas import AbstractRead

class FolderBase(BaseModel):
    title: str


class FolderCreate(FolderBase):
    pass


class FolderUpdate(FolderBase):
    pass


class FolderWithId(FolderBase):
    id: int


class FolderReadPublic(FolderWithId):
    class Config:
        orm_mode = True


class FolderWithAbstracts(FolderWithId):
    abstracts: List[AbstractRead]

    class Config:
        orm_mode = True
