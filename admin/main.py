from fastapi import FastAPI, Depends

from dependency_injector.wiring import inject, Provide

from admin.schemas import Login
from admin.containers import Container
from admin.services.authetication.authetication import AdminService

from admin.start.router import app as router_login
from admin.roles.router import router as router_roles


def create_app(title: str = 'default') -> FastAPI:
    container = Container()
    app = FastAPI(title=title)
    app.container = container
    app.include_router(router_login)
    app.include_router(router_roles)
    return app


admin_app = create_app('Admin Rec & Rem Backend')
