from src.repositories.builder_settings import RepositoriesSettingsBuilder, RepositoriesSettings

from src.abstract.models import Abstract
from src.folder.models import Folder
from src.workspace.models import Workspace


abstract_settings = (
    RepositoriesSettingsBuilder()
    .set_sqlalchemy_model(Abstract)
    .set_parent_model_id(Abstract.folder_id)
    .add_search_field(Abstract.title)
    .add_search_field(Abstract.description)
    .get_repository_settings()
)

folder_settings = (
    RepositoriesSettingsBuilder()
    .set_sqlalchemy_model(Folder)
    .set_parent_model_id(Folder.workspace_id)
    .add_search_field(Folder.title)
    .get_repository_settings()
)

workspace_settings = (
    RepositoriesSettingsBuilder()
    .set_sqlalchemy_model(Workspace)
    .add_search_field(Workspace.title)
    .add_search_field(Workspace.description)
    .get_repository_settings()
)
