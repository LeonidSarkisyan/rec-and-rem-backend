from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.services.databasemanager.builder import DataBaseManagerBuilder
from src.services.databasemanager.db import DataBaseOpenManager
from src.services.databasemanager.opening import OpenManagerRepository

from src.auth.models import User

from src.workspace.schemas import WorkspaceCreate, WorkspaceUpdate
from src.workspace.models import Workspace

from src.folder.models import Folder


#  workspace_database_manager = DataBaseOpenManager(Workspace, search_fields='title', use_user_id=True)

workspace_database_manager_builder = DataBaseManagerBuilder()

workspace_database_manager_builder.set_model(Workspace)
workspace_database_manager_builder.set_search_field('title')
workspace_database_manager_builder.set_child_field(Folder, Folder.workspace_id, 'workspace_id')

workspace_database_manager = workspace_database_manager_builder.get_database_manager()
