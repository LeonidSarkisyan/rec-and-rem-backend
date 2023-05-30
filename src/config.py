import enum

from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')


class AuthConfig:
    ACCESS_TOKEN_EXPIRE_MINUTES = 3600
    SECRET_KEY = os.environ.get('SECRET_AUTH')
    ALGORITHM = "HS256"


class YandexS3Config:
    AWS_ACCESS_KEY_ID = os.environ.get('YANDEX_S3_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('YANDEX_S3_SECRET_KEY')


class YandexS3Bucket:
    TEST = os.environ.get('BUCKET_TEST')


class YandexDirectories:
    AVATAR_PATH = os.environ.get('AVATAR_PATH')
    buckets = YandexS3Bucket









