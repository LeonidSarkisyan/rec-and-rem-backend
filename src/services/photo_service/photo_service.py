from fastapi import UploadFile
from fastapi.responses import StreamingResponse

import boto3

from src.config import YandexDirectories, YandexS3Config


session = boto3.session.Session()

s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=YandexS3Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=YandexS3Config.AWS_SECRET_ACCESS_KEY,
    region_name='ru-central1'
)

bucket = YandexDirectories.buckets.TEST


class ImageRepository:
    s3_client = s3

    @classmethod
    def upload_image(cls, file, key: str):
        cls.s3_client.upload_fileobj(file, Bucket=bucket, Key=key)

    @classmethod
    def download_image(cls, key: str):
        file = cls.s3_client.get_object(Bucket=bucket, Key=key)
        return StreamingResponse(file['Body'])


class PhotoService:
    s3_client = s3

    @classmethod
    def upload_photo(cls, file, url: str, entity: str) -> None:
        key = YandexDirectories.AVATAR_PATH + entity + url
        cls.s3_client.upload_fileobj(file, Bucket=bucket, Key=key)

    @classmethod
    def get_photo(cls, url: str, entity: str):
        key = YandexDirectories.AVATAR_PATH + entity + url
        try:
            file = cls.s3_client.get_object(Bucket=bucket, Key=key)
        except Exception:
            return cls.get_default_photo(entity)
        else:
            return StreamingResponse(file['Body'])

    @classmethod
    def get_default_photo(cls, entity: str):
        key = YandexDirectories.AVATAR_PATH + entity + 'chooseAvatar.png'
        file = cls.s3_client.get_object(Bucket=bucket, Key=key)
        return StreamingResponse(file['Body'])
