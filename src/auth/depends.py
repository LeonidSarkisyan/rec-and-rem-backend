from fastapi import Request, Depends

import jwt
from jwt.exceptions import DecodeError
from config import AuthConfig

from auth.routers.auth import UserDB

from database import get_async_session

from auth.exceptions.http import NoAuthorization
from auth.models import User


async def get_current_user(request: Request, session=Depends(get_async_session)) -> User:
    cookie_authorization: str = request.cookies.get("Authorization")
    try:
        data: dict = jwt.decode(cookie_authorization, key=AuthConfig.SECRET_KEY, algorithms=AuthConfig.ALGORITHM)
    except DecodeError:
        raise NoAuthorization
    user = await UserDB.get_user_by_email(data.get('sub'), session)
    return user
