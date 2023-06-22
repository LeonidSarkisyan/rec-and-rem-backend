from admin.config import AdminInfo

from admin.schemas import Login

from admin.repositories import BaseRepository

from admin.services.authetication.exceptions import UnprocessableEntity


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
        data['hashed_password'] = data.pop('password')
        data.update({'role_id': self._admin_info.ID})
        return await self._admin_repository.add_entity(data)

