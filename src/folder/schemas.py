from pydantic import BaseModel


class FolderBase(BaseModel):
    title: str


class FolderCreate(FolderBase):
    pass


class FolderUpdate(FolderBase):
    pass
