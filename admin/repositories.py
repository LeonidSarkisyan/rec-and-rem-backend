from src.repositories.builder_settings import RepositoriesSettingsBuilder, RepositoriesSettings
from src.repositories.repositories import BaseRepository


from src.auth.models import User, Role


admin_repository_settings = (
    RepositoriesSettingsBuilder()
    .set_sqlalchemy_model(User)
    .set_parent_model_id(User.role_id)
    .use_user(False)
    .add_ident_field(User.email)
    .get_repository_settings()
)

role_repository_settings = (
    RepositoriesSettingsBuilder()
    .set_sqlalchemy_model(Role)
    .use_user(False)
    .get_repository_settings()
)
