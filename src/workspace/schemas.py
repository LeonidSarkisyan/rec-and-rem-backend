from pydantic import BaseModel, validator
from src.schemas import make_optional


class WorkspaceBase(BaseModel):
    title: str
    description: str | None = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdateBase(WorkspaceBase):
    pass


WorkspaceUpdate = make_optional(WorkspaceUpdateBase)


class WorkspaceWithId(WorkspaceBase):
    id: int

    class Config:
        orm_mode = True


class WorkspaceRead(WorkspaceWithId):
    is_open: bool
    url_open: str | None


class WorkspaceReadPublic(WorkspaceRead):
    class Config:
        orm_mode = True
