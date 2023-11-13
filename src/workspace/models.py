from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

from src.folder.models import Folder


class Workspace(Base):
    __tablename__ = 'workspaces'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(60), nullable=True)
    is_open: Mapped[bool] = mapped_column(default=False)
    url_open: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    folders: Mapped["Folder"] = relationship(back_populates='workspace')
    workspace_avatars: Mapped["WorkspaceAvatar"] = relationship(back_populates='workspace')

    user: Mapped["User"] = relationship(back_populates='workspaces')


class WorkspaceAvatar(Base):
    __tablename__ = 'workspaces_avatars'

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_url: Mapped[str] = mapped_column(unique=True, nullable=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspaces.id', ondelete='CASCADE'), unique=True)

    workspace: Mapped[Workspace] = relationship(back_populates='workspace_avatars')

