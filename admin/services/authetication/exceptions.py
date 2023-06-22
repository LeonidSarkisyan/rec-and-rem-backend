from fastapi import HTTPException


UnprocessableEntity = HTTPException(status_code=422, detail='Неверный логин или пароль')
