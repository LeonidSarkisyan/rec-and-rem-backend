from fastapi import HTTPException

DefaultRoleNoDeletable = HTTPException(
    403,
    detail='Нельзя удалить роль по умолчанию!'
)
