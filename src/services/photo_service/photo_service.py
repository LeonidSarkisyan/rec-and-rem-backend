from fastapi import UploadFile


from src.config import YandexDirectories


class PhotoService:

    def __init__(self, s3) -> None:
        self.s3 = s3

    def upload_photo(self, file: UploadFile, url: str) -> None:
        bucket = YandexDirectories.buckets.TEST
        key = YandexDirectories.AVATAR_PATH + url
        self.s3.upload_fileobj(file.file, Bucket=bucket, Key=key)
