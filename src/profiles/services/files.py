import os

import uuid

from typing import List

from fastapi import UploadFile

from src.profiles.exceptions.http import InvalidExtensions


class FileManager:
    """ Класс для проверки файлов и их обработки до отправки на S3 сервис"""
    def __init__(self, files_ext: List[str]):
        self.files_ext = files_ext

    def is_valid_ext(self, ext: str):
        if ext not in self.files_ext:
            InvalidExtensions.set_allow_file_types('allow_types', self.files_ext)
            raise InvalidExtensions


photo_manager = FileManager(['.jpeg', '.jpg', '.png'])


def create_unique_filename(file: UploadFile):
    ext = os.path.splitext(file.filename)[1]
    photo_manager.is_valid_ext(ext)
    return uuid.uuid4().hex + ext
