from typing import List

from fastapi import HTTPException

ProfileAlreadyExist = HTTPException(status_code=409, detail='Профиль уже создан')


class CustomHTTPException(HTTPException):
    def set_allow_file_types(self, key: str, allowed_file_types: List[str]):
        self.detail[key] = allowed_file_types


InvalidExtensions = CustomHTTPException(
    status_code=415, detail={'detail': 'Некорректный тип файла!', 'allow_types': None}
)
