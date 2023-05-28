from fastapi import HTTPException

EmailAlreadyExists = HTTPException(
    status_code=409,
    detail='Такой email уже используется'
)

BadLoginOrPassword = HTTPException(
    status_code=403,
    detail='Неверный логин или пароль'
)

BadPasswordForChange = HTTPException(
    status_code=403,
    detail='Неверный пароль'
)

NoAuthorization = HTTPException(
        status_code=403,
        detail="Отсутствует авторизация"
)

NoAccess = HTTPException(
    status_code=403,
    detail='У вас нет прав доступа'
)
