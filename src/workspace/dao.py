from src.dao.base import BaseDAOService

from src.workspace.models import Workspace, WorkspaceAvatar
from src.workspace.sqlmaker import WorkspaceSQLMaker, WorkspaceAvatarSQLMaker

from src.folder.models import Folder


class WorkspaceDAO(BaseDAOService):
    model = Workspace
    search_fields = [Workspace.title, Workspace.description]
    sql_maker = WorkspaceSQLMaker
    have_user = True
    only_owner = True
    child_model = Folder
    child_parent_id = Folder.workspace_id
    child_name_parent_id = 'workspace_id'


class WorkspaceAvatarDAO(BaseDAOService):
    model = WorkspaceAvatar
    sql_maker = WorkspaceAvatarSQLMaker
    parent_id = WorkspaceAvatar.workspace_id
    parent_name_id = 'workspace_id'
