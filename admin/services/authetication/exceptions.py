from fastapi import HTTPException


UnprocessableEntity = HTTPException(status_code=422, detail='Неверный логин или пароль')

NotAdminRole = HTTPException(status_code=403, detail='Вы не являетесь администратором')
