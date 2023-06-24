import jwt
from jwt import DecodeError

from fastapi import Depends, Request
from src.database import get_async_session

from src.config import AuthConfig
from src.repositories.repositories import BaseRepository
from src.auth.models import User
from src.auth.exceptions.http import NoAuthorization
from src.database import Database, DATABASE_URL

from admin.repositories import admin_repository_settings
from admin.config import AdminInfo

from admin.services.authetication.exceptions import NotAdminRole


class AdminAuth:
    def __init__(self, admin_repository: BaseRepository):
        self._admin_repository = admin_repository

    async def __call__(self, request: Request) -> User:
        cookie_authorization: str = request.cookies.get("Authorization")
        try:
            data: dict = jwt.decode(cookie_authorization, key=AuthConfig.SECRET_KEY, algorithms=AuthConfig.ALGORITHM)
        except DecodeError:
            raise NoAuthorization
        admin = await self._admin_repository.get_entity_by_key('email', data.get('sub'))
        if admin.role_id != AdminInfo.ID:
            raise NotAdminRole
        return admin


get_admin = AdminAuth(BaseRepository(admin_repository_settings, Database(DATABASE_URL).session))

