from src.utils.randomizer import get_random_string
from src.utils.file import get_extensions

from src.services.photo_service.photo_service import ImageRepository


class ImageService:
    image_repository = ImageRepository

    @classmethod
    def upload_image(cls, file):
        key = 'abstracts/' + get_random_string() + '.' + get_extensions(file)
        print(key)
        cls.image_repository.upload_image(file.file, key)
        return key

    @classmethod
    def download_image(cls, key: str):
        return cls.image_repository.download_image(key)
