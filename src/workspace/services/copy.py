from src.services.copy_service import BaseCopyService
from src.workspace.dao import WorkspaceDAO


class WorkspaceCopyService(BaseCopyService):
    dao = WorkspaceDAO
