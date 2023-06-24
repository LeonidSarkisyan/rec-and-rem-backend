from fastapi import APIRouter, Depends, Response

from dependency_injector.wiring import inject, Provide

from admin.containers import Container
from admin.roles.services import RoleService

from admin.schemas import RoleCreate, RoleUpdate

from admin.dependencies import get_admin

from src.auth.models import User


router = APIRouter(tags=['Roles'], prefix='/roles')


@router.post('/')
@inject
async def create_default_roles(
    admin: User = Depends(get_admin),
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    print(admin)
    return await role_service.get_or_add_default_roles()


@router.get('/')
@inject
async def get_all_roles(
    admin: User = Depends(get_admin),
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.get_roles()


@router.post('/new')
@inject
async def create_new_role(
    role: RoleCreate,
    role_service: RoleService = Depends(Provide[Container.role_service]),
    admin: User = Depends(get_admin),
):
    return await role_service.create_role(role)


@router.delete('/')
@inject
async def delete_not_defaults_roles(
    admin: User = Depends(get_admin),
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.delete_not_defaults_roles()


@router.get('/{role_id}')
@inject
async def get_role(
    role_id: int,
    role_service: RoleService = Depends(Provide[Container.role_service]),
    admin: User = Depends(get_admin),
):
    return await role_service.get_role(role_id)


@router.patch('/{role_id}')
@inject
async def update_role(
    role_id: int,
    role: RoleUpdate,
    role_service: RoleService = Depends(Provide[Container.role_service]),
    admin: User = Depends(get_admin),
):
    return await role_service.update_role(role_id, role)


@router.delete('/{role_id}')
@inject
async def delete_role(
    role_id: int,
    role_service: RoleService = Depends(Provide[Container.role_service]),
    admin: User = Depends(get_admin),
):
    return await role_service.delete_role(role_id)
