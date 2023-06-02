from fastapi import Depends, UploadFile

from src.config import YandexDirectories

from src.depends import s3

from src.profiles.exceptions.http import NoAvatar


def upload_avatar_to_s3(file: UploadFile, url: str):
    bucket = YandexDirectories.buckets.TEST
    key = YandexDirectories.AVATAR_PATH + url
    s3.upload_fileobj(file.file, Bucket=bucket, Key=key)


def get_avatar_from_s3(url: str):
    bucket = YandexDirectories.buckets.TEST
    key = YandexDirectories.AVATAR_PATH + url
    try:
        object_s3 = s3.get_object(Bucket=bucket, Key=key)
    except Exception:
        raise NoAvatar
    return object_s3
