from dependency_injector import containers, providers

from src.database import DATABASE_URL, Database

from admin.services.authetication.authetication import AdminService, AdminInfo

from admin.roles.services import RoleService

from admin.repositories import admin_repository_settings, role_repository_settings

from src.repositories.repositories import BaseRepository


MODULES = [".start.router", ".roles.router"]


class Container(containers.DeclarativeContainer):

    db = providers.Singleton(Database, db_url=DATABASE_URL)

    wiring_config = containers.WiringConfiguration(modules=MODULES)

    admin_repository = providers.Factory(
        BaseRepository,
        session_factory=db.provided.session,
        settings=admin_repository_settings
    )

    admin_service = providers.Factory(
        AdminService,
        admin_info=AdminInfo(),
        admin_repository=admin_repository
    )

    role_repository = providers.Factory(
        BaseRepository,
        session_factory=db.provided.session,
        settings=role_repository_settings
    )

    role_service = providers.Factory(
        RoleService,
        admin_info=AdminInfo(),
        role_repository=role_repository,

    )



