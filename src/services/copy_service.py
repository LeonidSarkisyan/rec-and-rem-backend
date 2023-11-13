from src.exceptions.http import NotFound, AccessDenied, OwnEntity, NotValidCode, ErrorByCreating

from src.auth.models import User

from src.dao.base import BaseDAO
from src.utils.copy import duplicate_object


class _BaseCopyRepository:
    dao: BaseDAO = None

    @classmethod
    async def copy_record_object(
            cls,
            copy_object,
            user: User,
            parent_id: int = 0
    ):

        copy_object.user_id = user.id
        copy_object.is_open = False
        copy_object.url_open = ''
        data_dict = copy_object.__dict__
        del data_dict['_sa_instance_state']
        if parent_id:
            data_dict[cls.dao.parent_name_id] = parent_id
        new_object = await cls.dao.create(data_dict, cls.dao.model)
        return new_object

    @classmethod
    async def copy_children(cls, entity_id: int, new_entity, user: User):
        children = await cls.dao.get_children_by_id(entity_id)

        objects = []

        for child in children:
            copy_child = duplicate_object(child)
            copy_child.user_id = user.id
            copy_child.is_open = False
            copy_child.url_open = ''
            data_dict = copy_child.__dict__
            del data_dict['_sa_instance_state']
            data_dict[cls.dao.child_name_parent_id] = new_entity.id
            objects.append(data_dict)

        if objects:
            return children, await cls.dao.create_children(objects)


class BaseCopyService(_BaseCopyRepository):

    @classmethod
    async def copy_record(cls, entity, user: User, parent_id: int = 0):
        copy_object = duplicate_object(entity)
        if copy_object.user_id != user.id:
            new_object = await super().copy_record_object(copy_object, user, parent_id)
            return new_object
        else:
            raise OwnEntity
