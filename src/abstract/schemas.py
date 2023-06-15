from typing import Optional

from datetime import datetime

from pydantic import BaseModel

from src.schemas import make_optional


class AbstractBase(BaseModel):
    title: str
    description: Optional[str]
    content: Optional[str]


class AbstractCreate(AbstractBase):
    pass


class AbstractUpdateSchema(AbstractBase):
    content: str


AbstractUpdate = make_optional(AbstractUpdateSchema)


class AbstractWithId(AbstractBase):
    id: int


class AbstractRead(AbstractWithId):
    content: Optional[str]
    datetime_created: datetime
    datetime_updated: Optional[datetime]
    folder_id: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }
