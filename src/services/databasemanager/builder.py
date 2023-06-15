from src.services.databasemanager.db import DataBaseOpenManager
from src.services.databasemanager.exceptions import DoNotSetModel


class DataBaseManagerBuilder:
    def __init__(self):
        self.__database_manager = DataBaseOpenManager()
        self.ready_to_return: bool = False

    def set_model(self, model):
        self.__database_manager.Model = model
        self.ready_to_return = True
        return self

    def set_parent_model(self, model, parent_name_id: str):
        self.__database_manager.ParentModel = model
        self.__database_manager.parent_name_id = parent_name_id
        self.__database_manager.use_parent = True
        self.__database_manager.set_parent_type_database()
        return self

    def set_use_user(self, use_user: bool):
        self.__database_manager.use_user_id = use_user
        return self

    def set_search_field(self, search_field: str):
        self.__database_manager.search_field = search_field
        return self

    def get_database_manager(self):
        if self.ready_to_return:
            return self.__database_manager
        else:
            raise DoNotSetModel('Вы не установили модель для менеджера "set_model"')
