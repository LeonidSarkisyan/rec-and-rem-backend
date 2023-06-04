import datetime

from src.folder.models import Folder

from src.abstract.models import Abstract

from src.services.databasemanager.typesdatabase import TypeDataBase
from src.services.databasemanager.db import DataBaseOpenManager


abstract_database_manager = DataBaseOpenManager(Abstract, Folder, parent_name_id='folder_id', use_user_id=True)
abstract_database_manager.types_manager.set_type_database(
    TypeDataBase(datetime.datetime, lambda value: {'datetime_updated': value})
)

