from fastapi import HTTPException

ProfileAlreadyExist = HTTPException(status_code=409, detail='Профиль уже создан')