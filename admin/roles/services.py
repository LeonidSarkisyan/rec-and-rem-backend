from admin.config import AdminInfo

from admin.schemas import Login

from admin.constants import DEFAULT_ROLES, DEFAULT_ROLES_IDS

from admin.repositories import BaseRepository

from admin.schemas import RoleCreate, RoleUpdate

from admin.services.authetication.exceptions import UnprocessableEntity

from admin.roles.exceptions import DefaultRoleNoDeletable


class RoleService:

    def __init__(self, admin_info: AdminInfo, role_repository: BaseRepository):
        self._admin_info = admin_info
        self._role_repository = role_repository

    async def get_or_add_default_roles(self):
        roles = await self._role_repository.get_all_entities()
        if roles:
            return roles
        result = await self._role_repository.add_many_entities(DEFAULT_ROLES)
        return result

    async def get_roles(self):
        return await self._role_repository.get_all_entities()

    async def get_role(self, role_id: int):
        return await self._role_repository.get_entity_by_id(role_id)

    async def create_role(self, role: RoleCreate):
        data = role.dict()
        data['name'] = role.name.lower()
        result = await self._role_repository.add_entity(data)
        return result

    async def update_role(self, role_id: int, role: RoleUpdate):
        result = await self._role_repository.update_entity_by_id(role_id, role.dict())
        return result

    async def delete_role(self, role_id: int):
        if role_id in DEFAULT_ROLES_IDS:
            raise DefaultRoleNoDeletable
        result = await self._role_repository.delete_entity_by_id(role_id)
        return result

    async def delete_not_defaults_roles(self):
        ids = list(map(lambda role: role.id, await self._role_repository.get_ids_entities()))
        not_default_ids = [id_ for id_ in ids if id_ not in DEFAULT_ROLES_IDS]
        result = await self._role_repository.delete_entities_by_id(not_default_ids)
        return result

