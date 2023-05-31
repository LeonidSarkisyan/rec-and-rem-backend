from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends

from src.database import get_async_session, async_session_maker
from src.config import RolesId

from src.auth.models import Role as RoleModel


class Role:
    roles = {
        'admin': RolesId.ADMIN_ID,
        'moderator': RolesId.MODERATOR_ID,
        'user': RolesId.USER_ID
    }

    def __init__(self, name: str):
        self.name = name
        self.role_id = self.set_role_id()

    def set_role_id(self):
        return int(self.roles[self.name])

    def get_role_id(self) -> dict:
        return {"role_id": self.role_id}

    def is_this_role(self, role_id):
        return self.role_id == role_id

    def __repr__(self):
        return f'<Класс роли {self.name} id = {self.role_id}>'


class RolesSet:
    user = Role('user')
    moderator = Role('moderator')
    admin = Role('admin')
