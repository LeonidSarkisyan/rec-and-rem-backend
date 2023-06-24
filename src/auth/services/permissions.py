from typing import List

from fastapi import Request, Depends

from src.auth.models import User

from src.auth.depends import get_current_user

from src.auth.exceptions.http import NoAccess

from src.auth.services.rolesset import RolesSet, Role


class Permission:
    def __init__(self, roles: List[Role]):
        self.roles = roles

    def __call__(self, request: Request, user: User = Depends(get_current_user)):
        for role in self.roles:
            if user.role_id == role.role_id:
                return user
        raise NoAccess


get_valid_user = Permission(
    [RolesSet.user, RolesSet.moderator, RolesSet.admin]
)

get_valid_moderator = Permission(
    [RolesSet.moderator, RolesSet.admin]
)

get_valid_admin = Permission(
    [RolesSet.admin]
)
