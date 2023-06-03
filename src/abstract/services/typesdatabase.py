from typing import Callable


class TypeDataBase:
    """ Класс для подготовки данных с определённым типом """
    def __init__(self, some_type: str, function: Callable):
        self.type = some_type
        self.function = function

    def call_function(self):
        self.function(self.type)


def f(value):
    print('ТУТ ФУНКЦИЯ', value)


t = TypeDataBase('123', lambda x: print('Функция lambda', x))

t.call_function()

