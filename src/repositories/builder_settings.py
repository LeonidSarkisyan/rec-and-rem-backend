from typing import Type, TypeVar, Optional, Union, List

from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.database import Base

from src.abstract.models import Abstract
from src.folder.models import Folder
from src.workspace.models import Workspace

from src.repositories.exception import NotFoundIdentField


sqlalchemy_model_type = TypeVar("sqlalchemy_model_type", bound=Base)


class IdentsField:
    def __init__(self):
        self._keys: List[str] = []

    def add_property(self, column: InstrumentedAttribute):
        key_str = column.__dict__.get('key')
        setattr(self, key_str, column)
        self._keys.append(key_str)

    def get_property(self, key: str) -> InstrumentedAttribute:
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise NotFoundIdentField(key, self._keys)


class AdvancedModel:
    def __init__(self, model: Type[sqlalchemy_model_type]):
        self.real_model: Type[sqlalchemy_model_type] = model
        self.search_fields = []
        self.parent_id = None
        self.idents_fields = IdentsField()


class RepositoriesSettings:
    def __init__(self):
        self.model: Optional[AdvancedModel] = None
        self.use_search: bool = False
        self.use_parent: bool = False
        self.use_user: bool = True
        self.use_ident_fields: bool = False

    def __repr__(self):
        return f'RepositoriesSetting({self.model.real_model}, ' \
               f'parent_id = {self.model.parent_id}, ' \
               f'use_search = {self.use_search}, ' \
               f'use_user = {self.use_user})' \
               f'use_ident_fields = {self.use_ident_fields}'


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
            self.__settings.model.search_fields.append(search_field)
        else:
            self.__settings.model.search_fields.append(getattr(self.__settings.model.real_model, search_field))
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

    def add_ident_field(self, ident_field: InstrumentedAttribute):
        self.__settings.model.idents_fields.add_property(ident_field)
        self.__settings.use_ident_fields = True
        return self

    def get_repository_settings(self):
        if self.__ready_to_return:
            return self.__settings
        else:
            raise


from src.abstract.models import Abstract


a = IdentsField()
a.add_property(Abstract.id)
a.add_property(Abstract.title)

field = a.get_property('id')

print(field)