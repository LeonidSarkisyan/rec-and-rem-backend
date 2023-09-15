from datetime import datetime

from typing import List

from sqlalchemy import func

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime

from src.database import Base


class Abstract(Base):
    __tablename__ = 'abstracts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    content: Mapped[str] = mapped_column(nullable=True)
    datetime_created: Mapped[datetime] = mapped_column(server_default=func.now())
    datetime_updated: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    is_open: Mapped[bool] = mapped_column(default=False)
    url_open: Mapped[str] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    folder_id: Mapped[int] = mapped_column(ForeignKey('folders.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    folder: Mapped["Folder"] = relationship(back_populates='abstracts')
    user: Mapped["User"] = relationship(back_populates='abstracts')

