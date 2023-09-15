from fastapi import HTTPException

NotFound = HTTPException(status_code=404, detail='Не найдено')

AccessDenied = HTTPException(status_code=403, detail='Доступ запрещён')

OwnEntity = HTTPException(409, detail='Нельзя загружать свои материалы!')

NotValidCode = HTTPException(422, detail='Некорректный код')


class AgileHTTPException(HTTPException):
    def __init__(self, code, detail):
        super().__init__(code, detail)


ErrorByCreating = AgileHTTPException(422, 'Напишите название меньше 30 символов')