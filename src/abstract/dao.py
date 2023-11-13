from src.dao.base import BaseDAOService
from src.services.databasemanager.sqlquerymaker import BaseSQLMaker

from src.abstract.models import Abstract


class AbstractSQLMaker(BaseSQLMaker):
    model = Abstract


class AbstractDaoService(BaseDAOService):
    model = Abstract
    parent_id = Abstract.folder_id
    parent_name_id = 'folder_id'
    search_fields = [Abstract.title]
    have_user = True
    only_owner = True
    sql_maker = AbstractSQLMaker
