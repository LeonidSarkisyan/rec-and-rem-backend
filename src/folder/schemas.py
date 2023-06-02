from pydantic import BaseModel


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
