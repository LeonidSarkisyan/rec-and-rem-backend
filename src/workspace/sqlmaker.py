from src.services.databasemanager.sqlquerymaker import BaseSQLMaker

from src.workspace.models import Workspace, WorkspaceAvatar


class WorkspaceSQLMaker(BaseSQLMaker):
    model = Workspace


class WorkspaceAvatarSQLMaker(BaseSQLMaker):
    model = WorkspaceAvatar
