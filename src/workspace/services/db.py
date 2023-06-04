from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.services.databasemanager.db import DataBaseOpenManager
from src.services.databasemanager.opening import OpenManager

from src.auth.models import User

from src.workspace.schemas import WorkspaceCreate, WorkspaceUpdate
from src.workspace.models import Workspace


workspace_database_manager = DataBaseOpenManager(Workspace, search_field='title', use_user_id=True)

