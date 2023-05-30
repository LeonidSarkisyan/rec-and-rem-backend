import boto3
from src.config import YandexS3Config


def get_query_search(query_search: str = None):
    if query_search:
        return query_search.strip()


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=YandexS3Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=YandexS3Config.AWS_SECRET_ACCESS_KEY,
    region_name='ru-central1'
)
