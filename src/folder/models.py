from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from src.database import Base

from src.abstract.models import Abstract


class Folder(Base):
    __tablename__ = 'folders'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    is_open: Mapped[bool] = mapped_column(default=False)
    url_open: Mapped[str] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspaces.id', ondelete='CASCADE'), unique=False)

    user: Mapped["User"] = relationship(back_populates='folders')
    workspace: Mapped["Workspace"] = relationship(back_populates='folders')
    abstracts: Mapped["Abstract"] = relationship(back_populates='folder', cascade="all, delete", passive_deletes=True)
