from src.services.copy_service import BaseCopyService
from src.folder.dao import FolderDaoService


class FolderCopyService(BaseCopyService):
    dao = FolderDaoService
