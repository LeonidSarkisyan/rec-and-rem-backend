import json

from src.service import BaseService

from src.auth.models import User

from src.abstract.dao import AbstractDaoService
from src.abstract.copy import AbstractCopyService

from src.content.base import create_base_content


class AbstractService(BaseService):
    dao = AbstractDaoService
    copy = AbstractCopyService

    @classmethod
    async def copy_opened_entity_by_id(
            cls,
            entity_open_url: str,
            user: User,
            parent_id: int = 0
    ):
        abstract_id = await cls.open_manager.get_open_url(entity_open_url)
        abstract = await super().copy_opened_entity_by_id(abstract_id, user, parent_id)
        return abstract

    @classmethod
    async def create(cls, abstract, folder, user: User):
        data: dict = abstract.dict()
        data.update({'folder_id': folder.id})
        data.update({'user_id': user.id})
        data.update({'content': create_base_content()})
        return await cls.dao.create(data)

    @classmethod
    async def get_content(
            cls,
            abstract_id: int,
            user: User
    ):
        abstract = await cls.dao.get_entity_by_id(abstract_id)
        cls.validator.is_owner(abstract, user)
        return abstract.content

    @classmethod
    async def set_content(cls, content: str, abstract_id: int, user: User):
        content_json = json.loads(content)
        result = await cls.dao.update(
            {"content": content_json}, cls.dao.model.id == abstract_id, cls.dao.model.user_id == user.id
        )
        return result
