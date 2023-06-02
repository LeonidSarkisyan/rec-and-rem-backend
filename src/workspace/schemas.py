from pydantic import BaseModel, validator


class WorkspaceBase(BaseModel):
    title: str
    description: str | None = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    pass


class WorkspaceWithId(WorkspaceBase):
    id: int

    class Config:
        orm_mode = True


class WorkspaceReadPublic(WorkspaceWithId):
    class Config:
        orm_mode = True


class WorkspaceRead(WorkspaceWithId):
    is_open: bool
