from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.schemas import UserCreate
from auth.models import User
from auth.exceptions.http import EmailAlreadyExists
from auth.services.hashing import Hash

from fastapi import Request
from fastapi import HTTPException
from fastapi import status

from typing import Optional
from typing import Dict

from auth.services.rolesset import RolesSet
from auth.models import Role


class UserDB:

    @staticmethod
    async def get_users(query_search: str, session: AsyncSession):
        if query_search:
            query = select(User).where(User.email.ilike('%' + query_search + '%')).options(selectinload(User.role))
        else:
            query = select(User).options(selectinload(User.role))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def add_user(user: UserCreate, session: AsyncSession):
        try:
            user.hashed_password = Hash.bcrypt(user.hashed_password)

            data = user.dict() | RolesSet.user.get_role_id()  # role user

            stmt = insert(User).returning(User.id).values(**data)
            result = await session.execute(stmt)
            id_new_user = result.first()
            await session.commit()
        except IntegrityError:
            raise EmailAlreadyExists
        else:
            return id_new_user[0]

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(user_email: str, session: AsyncSession) -> User:
        query = select(User).where(User.email == user_email).options(selectinload(User.role))
        result = await session.execute(query)
        return result.scalars().first()

