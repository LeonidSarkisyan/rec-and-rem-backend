from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Workspace(Base):
    __tablename__ = 'workspaces'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_open: Mapped[bool] = mapped_column(default=False)
    url_open: Mapped[str] = mapped_column(default='')

    user: Mapped["User"] = relationship(back_populates='workspaces')
