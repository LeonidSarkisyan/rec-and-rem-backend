from PIL import Image

from fastapi import UploadFile, Depends

from dependency_injector.wiring import inject, Provide

from src.containers import Container

from src.services.databasemanager.opening import OpenManagerService
from src.services.copy_service import BaseCopyService
from src.services.photo_handler import PhotoHandler

from src.utils.randomizer import get_random_string
from src.utils.file import get_extensions

from src.dao.validator import Validator
from src.dao.base import BaseDAOService

from src.auth.models import User


class BaseService:
    dao: BaseDAOService = None
    copy: BaseCopyService = None
    validator: Validator = Validator
    open_manager: OpenManagerService = OpenManagerService
    photo_manager: PhotoHandler = PhotoHandler

    @classmethod
    async def copy_opened_entity_by_id(
            cls,
            entity_id: int,
            user: User,
            parent_id: int = 0
    ):
        entity = await cls.dao.get_entity_by_id(entity_id)

        cls.validator.is_exist(entity)
        cls.validator.is_open(entity)

        new_object = await cls.copy.copy_record(entity, user, parent_id)

        return new_object

    @classmethod
    async def mark_as_delete_entity(
            cls,
            entity_id,
            mark_deleted: bool,
            user: User
    ):
        deleted_model = await cls.dao.mark_as_delete_entity(
            mark_deleted, cls.dao.model.id == entity_id, cls.dao.model.user_id == user.id
        )
        cls.validator.is_exist(deleted_model)

    @classmethod
    async def upload_avatar(
            cls,
            entity_id: int,
            file: UploadFile
    ):
        if cls.photo_manager.validator.is_photo(file):
            unique_url, ext = cls.photo_manager.create_unique_filename(file)
            updated_data = {
                "photo_url": unique_url + '.' + ext,
                cls.dao.parent_name_id: entity_id,
            }
            await cls.dao.create_or_update_by_id(updated_data, cls.dao.parent_id == entity_id)
            compressed_file = cls.photo_manager.compress_img(file.file)
            cls.photo_manager.s3_service.upload_photo(compressed_file, updated_data["photo_url"], 'workspaces/')

    @classmethod
    async def get_avatar(cls, entity_id: int):
        avatar = await cls.dao.get_entity_by_filters(cls.dao.parent_id == entity_id)
        if avatar and avatar.photo_url:
            return cls.photo_manager.s3_service.get_photo(avatar.photo_url,  'workspaces/')
        else:
            return cls.photo_manager.s3_service.get_default_photo('workspaces/')
