from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import UserCreate
from auth.models import User
from auth.exceptions.http import EmailAlreadyExists


class UserDB:
    @staticmethod
    async def add_user(user: UserCreate, session: AsyncSession):
        try:
            stmt = insert(User).returning(User.id).values(**user.dict())
            result = await session.execute(stmt)
            id_new_user = result.first()
            await session.commit()
        except IntegrityError:
            raise EmailAlreadyExists
        else:
            return id_new_user[0]
