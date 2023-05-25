from fastapi import HTTPException

EmailAlreadyExists = HTTPException(
    status_code=409,
    detail='Такой email уже используется'
)
