from typing import Type, TypeVar, Optional, Union

from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.database import Base

from src.abstract.models import Abstract
from src.folder.models import Folder
from src.workspace.models import Workspace


sqlalchemy_model_type = TypeVar("sqlalchemy_model_type", bound=Base)


class AdvancedModel:
    def __init__(self, model: Type[sqlalchemy_model_type]):
        self.real_model: Type[sqlalchemy_model_type] = model
        self.search_field = []
        self.parent_id = None


class RepositoriesSettings:
    def __init__(self):
        self.model: Optional[AdvancedModel] = None
        self.use_search: bool = False
        self.use_parent: bool = False
        self.use_user: bool = True

    def __repr__(self):
        return f'RepositoriesSetting({self.model.real_model}, ' \
               f'parent_id = {self.model.parent_id}, ' \
               f'use_search = {self.use_search}, ' \
               f'use_user = {self.use_user})'


class RepositoriesSettingsBuilder:
    def __init__(self):
        self.__settings = RepositoriesSettings()
        self.__ready_to_return: bool = False

    def set_sqlalchemy_model(self, model: Type[sqlalchemy_model_type]):
        self.__settings.model = AdvancedModel(model)
        self.__ready_to_return = True
        return self

    def add_search_field(self, search_field: Union[InstrumentedAttribute, str]):
        if type(search_field) == InstrumentedAttribute:
            self.__settings.model.search_field.append(search_field)
        else:
            self.__settings.model.search_field.append(getattr(self.__settings.model.real_model, search_field))
        self.__settings.use_search = True
        return self

    def set_parent_model_id(self, parent_id: Union[InstrumentedAttribute, str]):
        if type(parent_id) == InstrumentedAttribute:
            self.__settings.model.parent_id = parent_id
        else:
            self.__settings.model.parent_id = getattr(self.__settings.model.real_model, parent_name_id)
        self.__settings.use_parent = True
        return self

    def use_user(self, use_user: bool):
        self.__settings.use_user = use_user
        return self

    def get_repository_settings(self):
        if self.__ready_to_return:
            return self.__settings
        else:
            raise



