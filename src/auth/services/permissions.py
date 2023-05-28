from typing import List

from fastapi import Request, Depends

from auth.models import User

from auth.depends import get_current_user

from auth.exceptions.http import NoAccess

from auth.services.rolesset import RolesSet, Role


class Permission:
    def __init__(self, roles: List[Role]):
        self.roles = roles

    def __call__(self, request: Request, user: User = Depends(get_current_user)):
        for role in self.roles:
            if user.role_id == role.role_id:
                return user
        raise NoAccess


user_permission = Permission(
    [RolesSet.user, RolesSet.moderator, RolesSet.admin]
)

moderator_permission = Permission(
    [RolesSet.moderator, RolesSet.admin]
)

admin_permission = Permission(
    [RolesSet.admin]
)
