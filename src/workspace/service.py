import time

from src.services.databasemanager.opening import OpenManagerService
from src.dao.validator import Validator
from src.service import BaseService
from src.database import async_session_maker

from src.auth.models import User

from src.workspace.dao import WorkspaceDAO, WorkspaceAvatarDAO
from src.workspace.services.copy import WorkspaceCopyService

from src.folder.service import FolderCopyService


class WorkspaceService(BaseService):
    dao = WorkspaceDAO
    copy = WorkspaceCopyService
    child_copy = FolderCopyService

    @classmethod
    async def copy_opened_entity_by_id(
            cls,
            entity_open_url: str,
            user: User,
            parent_id: int = 0
    ):
        entity_id = await cls.open_manager.get_open_url(entity_open_url)
        workspace = await super().copy_opened_entity_by_id(entity_id, user, parent_id)
        old_folders, new_folders = await cls.copy.copy_children(entity_id, workspace, user)
        for old_folder, new_folder in zip(old_folders, new_folders):
            await cls.child_copy.copy_children(old_folder.id, new_folder, user)
        return workspace


class WorkspaceAvatarService(BaseService):
    dao = WorkspaceAvatarDAO

