import datetime

from src.folder.models import Folder

from src.abstract.models import Abstract

from src.services.databasemanager.typesdatabase import TypeDataBase
from src.services.databasemanager.db import DataBaseOpenManager
from src.services.databasemanager.builder import DataBaseManagerBuilder


# abstract_database_manager = DataBaseOpenManager(Abstract, Folder, parent_name_id='folder_id', use_user_id=True)
# abstract_database_manager.types_manager.set_type_database(
#     TypeDataBase(datetime.datetime, lambda value: {'datetime_updated': value})
# )

abstract_database_manager_builder = DataBaseManagerBuilder()
abstract_database_manager_builder.set_model(Abstract)
abstract_database_manager_builder.set_parent_model(Folder, 'folder_id')

abstract_database_manager = abstract_database_manager_builder.get_database_manager()

abstract_database_manager.types_manager.set_type_database(
    TypeDataBase(datetime.datetime, lambda value: {'datetime_updated': value})
)
