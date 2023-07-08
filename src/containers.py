from src.config import YandexS3Config


from dependency_injector import containers, providers

import boto3

from src.services.photo_service.photo_service import PhotoService


MODULES = ['.profiles.router']


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=MODULES)

    s3_session = providers.Singleton(
        boto3.session.Session
    )

    s3_client = providers.Singleton(
        s3_session.provided.client,
        service_name="s3",
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central1',
        aws_access_key_id=YandexS3Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=YandexS3Config.AWS_SECRET_ACCESS_KEY,
    )

    photo_service = providers.Factory(
        PhotoService,
        s3=s3_client
    )
