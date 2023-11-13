from typing import Union

from io import BytesIO

from tempfile import SpooledTemporaryFile

import os
import sys

from fastapi import UploadFile

from PIL import Image

from src.services.photo_service.photo_service import PhotoService

from src.utils.file import get_extensions
from src.utils.randomizer import get_random_string


def image_to_byte_array(image: Image) -> bytes:
    img_bytes = BytesIO()
    image.save(img_bytes, format=image.format)
    img_bytes = img_bytes.getvalue()
    return img_bytes


class PhotoValidator:
    photo_extensions = ['png', 'jpg', 'jpeg']

    @classmethod
    def is_photo(cls, file: UploadFile) -> (bool, str):
        ext = get_extensions(file)
        return ext.lower() in cls.photo_extensions, ext


class PhotoHandler:
    validator: PhotoValidator = PhotoValidator
    s3_service: PhotoService = PhotoService

    @classmethod
    def create_unique_filename(cls, file: UploadFile) -> (str, str):
        unique_url = get_random_string(50)
        ext = get_extensions(file)
        return unique_url, ext

    @classmethod
    def find_memory_upload(cls, file: UploadFile) -> float:
        file = Image.open(file.file)
        img_file_size_png = cls.find_memory_image(file)
        file.close()
        return img_file_size_png

    @classmethod
    def find_memory_image(cls, file) -> float:
        img_file = BytesIO()
        file.save(img_file, 'png')
        img_file_size_png = img_file.tell()
        file.close()
        return img_file_size_png

    @classmethod
    def compress(cls, file: UploadFile, new_size_ratio):
        print(cls.find_memory_upload(file))
        with Image.open(file.file) as image:
            new_image = image.resize((int(image.size[0] * new_size_ratio), int(image.size[1] * new_size_ratio)))
            print(cls.find_memory_image(new_image))

    @classmethod
    def compress_img(
            cls,
            file: SpooledTemporaryFile | BytesIO,
            new_size_ratio: float = 0.9,
            size_limit_mb: float = 0.2
    ) -> BytesIO:
        file_to_resize = file
        print(sys.getsizeof(file) / 1024 / 1024)
        while True:
            img = Image.open(file_to_resize)
            format_file = img.format
            img = img.resize((int(img.width * new_size_ratio), (int(img.height * new_size_ratio))))
            img.format = format_file
            image_array = BytesIO(image_to_byte_array(img))
            size = sys.getsizeof(image_array) / 1024 / 1024
            print('-' * 100)
            print(size)
            print('-' * 100)
            new_size_ratio -= 0.05
            if size < size_limit_mb:
                break
        return image_array
