from fastapi import Request

import jwt
from jwt.exceptions import DecodeError
from config import AuthConfig

from auth.exceptions.http import NoAuthorization


async def get_current_user(request: Request):
    cookie_authorization: str = request.cookies.get("Authorization")
    try:
        data = jwt.decode(cookie_authorization, key=AuthConfig.SECRET_KEY, algorithms=AuthConfig.ALGORITHM)
    except DecodeError:
        raise NoAuthorization
    return data
