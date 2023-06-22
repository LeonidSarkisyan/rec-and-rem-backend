from fastapi import APIRouter, Depends, Response

from dependency_injector.wiring import inject, Provide

from admin.containers import Container
from admin.roles.services import RoleService

from admin.schemas import RoleCreate


router = APIRouter(tags=['Roles'], prefix='/roles')


@router.post('/')
@inject
async def create_default_roles(
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.get_or_add_default_roles()


@router.get('/')
@inject
async def get_all_roles(
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.get_roles()


@router.post('/new')
@inject
async def create_new_role(
    role: RoleCreate,
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.create_role(role)


@router.delete('/')
@inject
async def delete_not_defaults_roles(
    role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.delete_not_defaults_roles()
