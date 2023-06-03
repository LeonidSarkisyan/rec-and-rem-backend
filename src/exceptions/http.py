from fastapi import HTTPException

NotFound = HTTPException(status_code=404, detail='Не найдено')

AccessDenied = HTTPException(status_code=403, detail='Доступ запрещён')
