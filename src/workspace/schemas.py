from pydantic import BaseModel, validator


class WorkspaceBase(BaseModel):
    title: str


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    id: int
    is_open: bool

    class Config:
        orm_mode = True
