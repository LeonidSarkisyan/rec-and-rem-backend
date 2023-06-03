from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class AbstractBase(BaseModel):
    title: str
    description: str


class AbstractCreate(AbstractBase):
    pass


class AbstractWithId(AbstractBase):
    id: int


class AbstractRead(AbstractWithId):
    content: Optional[str]
    datetime_created: datetime
    datetime_updated: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }
