from fastapi import APIRouter, Depends, Response

from dependency_injector.wiring import inject, Provide

from admin.schemas import Login
from admin.containers import Container
from admin.services.authetication.authetication import AdminService

app = APIRouter(tags=['Login'], prefix='/account')


@app.post('/')
@inject
async def login_in_root(
        login: Login,
        response: Response,
        admin_service: AdminService = Depends(Provide[Container.admin_service]),
):
    clear_login = await admin_service.authenticate(login)
    admin_user = await admin_service.get_or_create_root_admin(login)
    return admin_user
