from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import DBAPIError

from fastapi import HTTPException

from src.exceptions.http import NotFound, AccessDenied, OwnEntity, NotValidCode, ErrorByCreating

from src.services.databasemanager.sqlquerymaker import default_sql_query_maker
from src.services.databasemanager.exceptions import NotUseParentModel
from src.services.databasemanager.typesdatabase import TypeDataBase, TypeDataBaseManager
from src.services.databasemanager.opening import OpenManager

from src.auth.models import User

from src.utils.copy import duplicate_object


class DataBaseManager:
    """
        A generic class that performs CRUD operations.
        But it has advanced functionality in the form of access, advanced select.
    """
    def __init__(self):
        self.Model = None
        self.ParentModel = None
        self.parent_name_id = None
        self.search_field = None

        self.use_user_id = True
        self.types_manager = TypeDataBaseManager(load_default_types=True)
        self.use_parent: bool = False

    def set_parent_type_database(self):
        parent_type_database = TypeDataBase(self.ParentModel, lambda value: {self.parent_name_id: value.id})
        self.types_manager.set_type_database(parent_type_database)

    def prepare_data_before_create(self, data):
        clean_data = {}
        for one_data in data:
            for type_data_base in self.types_manager:
                result: dict = type_data_base.prepare_value(one_data)
                if result:
                    clean_data.update(result)
                    break
        return clean_data

    async def add_entity(self, *data, user: User, session: AsyncSession):
        clean_data: dict = self.prepare_data_before_create(data)

        if self.use_user_id:
            clean_data.update({'user_id': user.id})

        stmt = insert(self.Model).returning(self.Model.id).values(**clean_data)
        try:
            result = await session.execute(stmt)
        except DBAPIError as e:
            raise ErrorByCreating
        await session.commit()
        return result.scalar()

    async def get_entities(self, user: User, session: AsyncSession, filter_value: int = None, search_query: str = None):

        if filter_value and not self.use_parent:
            raise NotUseParentModel('Вы пытаетесь использовать id родителя без его определения при создании объекта')

        if self.use_parent:
            compare_attribute = getattr(self.Model, self.parent_name_id)
        elif self.use_user_id:
            compare_attribute = self.Model.user_id
            filter_value = user.id
        else:
            compare_attribute = None
        query = default_sql_query_maker.select(
            self.Model,
            self.search_field,
            compare_attribute,
            filter_value,
            search_query
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_entity_by_id(self, entity_id: int, user: User, session: AsyncSession, only_owner: bool = True):
        query = select(self.Model).where(self.Model.id == entity_id)
        result = await session.execute(query)
        entity = result.scalar()
        return await self.validate_before_send(entity, user, only_owner)

    async def update_entity_by_id(self, *data, entity_id: int, user: User, session: AsyncSession):
        clean_data: dict = self.prepare_data_before_create(data)
        clean_data = {key: value for key, value in clean_data.items() if value}
        stmt = update(self.Model).returning(self.Model.user_id).where(self.Model.id == entity_id).values(**clean_data)
        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return 'success'

    async def delete_entity_by_id(self, entity_id: int, user: User, session: AsyncSession):
        stmt = delete(self.Model).returning(self.Model.user_id).where(self.Model.id == entity_id)
        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise AccessDenied
        else:
            await session.commit()
        return 'success'

    @staticmethod
    async def validate_before_send(entity, user, only_owner):
        if not entity:
            raise NotFound

        if only_owner:
            if entity.user_id != user.id:
                raise AccessDenied

        return entity


class DataBaseOpenManager(DataBaseManager):
    """
        Extends the shared class by adding the ability to open/close entities in shared access.
        Models must have two required attributes: url_open: str, is_open: bool.
    """
    @staticmethod
    async def get_unique_url(entity_id: int, user: User, session: AsyncSession, count_symbols: int = 10):
        unique_url: str = await OpenManager.create_open_url(entity_id, n=count_symbols)
        return unique_url

    async def open_or_close_entity_by_id(
            self, entity_id: int, user: User, session: AsyncSession, is_open: bool, count_symbols: int = 10
    ):
        unique_url: str = await OpenManager.create_open_url(entity_id, n=count_symbols) if is_open else ''

        data = {
            "url_open": unique_url,
            "is_open": is_open
        }

        stmt = update(self.Model)\
            .where(self.Model.id == entity_id)\
            .values(**data)\
            .returning(self.Model.user_id)

        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise AccessDenied
        else:
            await session.commit()
        return {'unique_url': f'{unique_url}'}

    async def get_public_entity_by_id(
            self,
            entity_open_url: str,
            user: User,
            session: AsyncSession,
            copy: bool = False,
            count_symbols: int = 12,
            parent_id: int = None
    ):
        try:
            entity_id = await OpenManager.get_entity_id(entity_open_url)
        except ValueError:
            raise NotValidCode

        query = select(self.Model).where(self.Model.id == entity_id)
        try:
            result = await session.execute(query)
        except DBAPIError:
            raise NotValidCode

        entity = result.scalar()
        if not entity:
            raise HTTPException(status_code=404, detail='Не найдено')
        if not entity.is_open:
            raise HTTPException(status_code=404, detail='Не найдено')

        if copy:
            copy_object = duplicate_object(entity)
            if copy_object.user_id != user.id:
                copy_object.user_id = user.id
                copy_object.is_open = False
                copy_object.url_open = ''
                data_dict = copy_object.__dict__
                del data_dict['_sa_instance_state']
                if parent_id:
                    data_dict[self.parent_name_id] = parent_id
                print(data_dict)
                stmt = insert(self.Model).returning(self.Model).values(**data_dict)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
            else:
                raise OwnEntity

        return entity
