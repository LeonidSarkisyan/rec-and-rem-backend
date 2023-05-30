from fastapi import Depends, UploadFile

from src.config import YandexDirectories

from src.depends import s3


def upload_avatar_to_s3(file: UploadFile, url: str):
    bucket = YandexDirectories.buckets.TEST
    key = YandexDirectories.AVATAR_PATH + url
    s3.upload_fileobj(file.file, Bucket=bucket, Key=key)


def get_avatar_from_s3(url: str):
    bucket = YandexDirectories.buckets.TEST
    key = YandexDirectories.AVATAR_PATH + url
    return s3.get_object(Bucket=bucket, Key=key)
