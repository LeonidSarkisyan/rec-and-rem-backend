from src.services.databasemanager.db import DataBaseOpenManager
from src.services.databasemanager.builder import DataBaseManagerBuilder

from src.workspace.models import Workspace

from src.folder.models import Folder


folder_database_manager_builder = DataBaseManagerBuilder()

folder_database_manager_builder.set_model(Folder)
folder_database_manager_builder.set_search_field('title')

folder_database_manager_builder.set_parent_model(Workspace, 'workspace_id')

folder_database_manager = folder_database_manager_builder.get_database_manager()
