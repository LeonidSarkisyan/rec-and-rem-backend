from fastapi import Request, Depends

import jwt
from jwt.exceptions import DecodeError
from src.config import AuthConfig

from src.auth.routers.auth import UserDB

from src.database import get_async_session

from src.auth.exceptions.http import NoAuthorization, NoAccess
from src.auth.models import User

from src.auth.services.rolesset import RolesSet


async def get_current_user(request: Request, session=Depends(get_async_session)) -> User:
    cookie_authorization: str = request.cookies.get("Authorization")
    try:
        data: dict = jwt.decode(cookie_authorization, key=AuthConfig.SECRET_KEY, algorithms=AuthConfig.ALGORITHM)
    except DecodeError:
        raise NoAuthorization
    user = await UserDB.get_user_by_email(data.get('sub'), session)
    return user


async def get_current_profile(request: Request, session=Depends(get_async_session)):
    cookie_authorization: str = request.cookies.get("Authorization")
    try:
        data: dict = jwt.decode(cookie_authorization, key=AuthConfig.SECRET_KEY, algorithms=AuthConfig.ALGORITHM)
    except DecodeError:
        raise NoAuthorization
    user = await UserDB.get_user_by_email(data.get('sub'), session)
    return user
