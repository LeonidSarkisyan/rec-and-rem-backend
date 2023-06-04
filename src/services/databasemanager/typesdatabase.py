import datetime
from typing import Callable, List
from pydantic import BaseModel


class TypeDataBase:
    """ Класс для подготовки данных с определённым типом """
    def __init__(self, some_type, function: Callable):
        self.type = some_type
        self.function = function

    def prepare_value(self, value):
        if isinstance(value, self.type):
            return self.function(value)


default_type_database = [
    TypeDataBase(BaseModel, lambda value: value.dict()),
    TypeDataBase(dict, lambda value: value),
]


class TypeDataBaseManager:
    def __init__(self, load_default_types=True):
        self.types: List[TypeDataBase] = []
        if load_default_types:
            self.types.extend(default_type_database)

    def set_type_database(self, type_database: TypeDataBase):
        self.types.append(type_database)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            type_data_base = self.types[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        else:
            return type_data_base



