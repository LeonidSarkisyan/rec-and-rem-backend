from src.dao.base import BaseDAOService
from src.services.databasemanager.sqlquerymaker import BaseSQLMaker

from src.folder.models import Folder

from src.abstract.models import Abstract


class FolderSQLMaker(BaseSQLMaker):
    model = Folder


class FolderDaoService(BaseDAOService):
    model = Folder
    parent_id = Folder.workspace_id
    parent_name_id = 'workspace_id'
    search_fields = [Folder.title]
    have_user = True
    only_owner = True
    sql_maker = FolderSQLMaker
    child_model = Abstract
    child_parent_id = Abstract.folder_id
    child_name_parent_id = 'folder_id'
