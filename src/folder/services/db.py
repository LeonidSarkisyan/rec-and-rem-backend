from src.services.databasemanager.db import DataBaseOpenManager

from src.workspace.models import Workspace

from src.folder.models import Folder


folder_database_manager = DataBaseOpenManager(Folder, Workspace, parent_name_id='workspace_id', use_user_id=True)
