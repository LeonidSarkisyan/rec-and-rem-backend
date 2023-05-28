from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), index=True, nullable=True)
    second_name: Mapped[str] = mapped_column(String(30), nullable=True)
    username: Mapped[str] = mapped_column(String(30), nullable=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True, unique=True)

    user: Mapped["User"] = relationship(back_populates='profile')
