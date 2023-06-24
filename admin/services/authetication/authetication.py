from datetime import timedelta

from src.config import AuthConfig

from src.auth.services.auth import create_access_token

from admin.config import AdminInfo

from admin.schemas import Login

from admin.repositories import BaseRepository

from admin.services.authetication.exceptions import UnprocessableEntity

from admin.utils.hashing import Hash

from sqlalchemy.exc import IntegrityError


class AdminService:
    def __init__(self, admin_info: AdminInfo, admin_repository: BaseRepository):
        self._admin_info = admin_info
        self._admin_repository = admin_repository

    async def authenticate(self, login: Login) -> Login:
        if login.email != self._admin_info.ADMIN_LOGIN:
            raise UnprocessableEntity
        if login.password != self._admin_info.ADMIN_PASS:
            raise UnprocessableEntity
        return login

    async def get_or_create_root_admin(self, login: Login):
        data: dict = login.dict()
        data['hashed_password'] = Hash.to_hash(data.pop('password'))
        data.update({'role_id': self._admin_info.ID})
        try:
            await self._admin_repository.add_entity(data)
        except IntegrityError:
            print('Админ уже создан!')
        else:
            print('Админ только что создан')
        return data

    @staticmethod
    async def get_access_token(login: Login):
        access_token_expires = timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": login.email}, expires_delta=access_token_expires
        )
        return access_token


