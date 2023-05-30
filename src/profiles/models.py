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
    avatar: Mapped["Avatar"] = relationship(back_populates='profile', uselist=False)


class Avatar(Base):
    __tablename__ = 'avatars'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    profile_id: Mapped[int] = mapped_column(ForeignKey('profiles.id'), unique=True)

    profile: Mapped["Profile"] = relationship(back_populates='avatar')

