from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

# Костыль! (Наверное)
from src.workspace.models import Workspace


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()

    users: Mapped[List["User"]] = relationship(back_populates='role')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))

    role: Mapped["Role"] = relationship(back_populates='users')
    workspaces: Mapped[List["Workspace"]] = relationship(back_populates='user')
    profile: Mapped["Profile"] = relationship(back_populates='user', uselist=False)

