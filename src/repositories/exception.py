
class MyCustomError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'{self.message}'
        else:
            return f'Что-то пошло не так'


class DoNotSetModel(Exception):
    pass


class NotFoundIdentField(MyCustomError):
    def __init__(self, key, keys):
        self.message = f'Не найдено поле идентификации {key}, доступные поля = {keys}'
