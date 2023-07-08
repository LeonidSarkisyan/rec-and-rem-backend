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
    admin_user = await admin_service.get_or_create_root_admin(clear_login)
    access_token = await admin_service.get_access_token(clear_login)
    response.set_cookie(key="Authorization", value=f"{access_token}", httponly=True)
    return admin_user
