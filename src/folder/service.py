from src.service import BaseService

from src.auth.models import User

from src.folder.dao import FolderDaoService
from src.folder.services.copy import FolderCopyService


class FolderService(BaseService):
    dao = FolderDaoService
    copy = FolderCopyService

    @classmethod
    async def copy_opened_entity_by_id(
            cls,
            entity_open_url: str,
            user: User,
            parent_id: int = 0
    ):
        folder_id = await cls.open_manager.get_open_url(entity_open_url)
        folder = await super().copy_opened_entity_by_id(folder_id, user, parent_id)
        await cls.copy.copy_children(folder_id, folder, user)
        return folder
