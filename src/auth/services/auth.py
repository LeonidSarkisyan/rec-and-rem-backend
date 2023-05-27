from datetime import datetime, timedelta

import jwt

from sqlalchemy.ext.asyncio import AsyncSession

from auth.services.db import UserDB
from auth.services.hashing import Hash

from auth.exceptions.http import BadLoginOrPassword

from config import AuthConfig


class UserAuth:
    @staticmethod
    async def authenticate_user(email: str, password: str, session: AsyncSession):
        user = await UserDB.get_user_by_email(email, session)
        if not user:
            raise BadLoginOrPassword
        if not Hash.verify(user.hashed_password, password):
            raise BadLoginOrPassword
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)
    return encoded_jwt




