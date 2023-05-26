from fastapi import Request

import jwt

from config import AuthConfig

from auth.exceptions.http import NoAuthorization


async def get_current_user(request: Request):
    cookie_authorization: str = request.cookies.get("Authorization")
    data = jwt.decode(cookie_authorization, key=AuthConfig.SECRET_KEY, algorithms=AuthConfig.ALGORITHM)
    return data
