from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import UserCreate
from auth.models import User
from auth.exceptions.http import EmailAlreadyExists
from auth.services.hashing import Hash

from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from typing import Dict


class UserDB:
    @staticmethod
    async def add_user(user: UserCreate, session: AsyncSession):
        try:
            user.hashed_password = Hash.bcrypt(user.hashed_password)
            stmt = insert(User).returning(User.id).values(**user.dict())
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
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        return result.scalars().first()
