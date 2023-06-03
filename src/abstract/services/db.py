from src.folder.models import Folder

from src.abstract.models import Abstract

from src.services.db import DataBaseManager


abstract_database_manager = DataBaseManager(Abstract, Folder, parent_name_id='folder_id', use_user_id=True)
