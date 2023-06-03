from typing import List

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from fastapi import HTTPException

from src.exceptions.http import NotFound, AccessDenied

from src.services.typesdatabase import TypeDataBase, default_type_database, TypeDataBaseManager
from src.services.opening import OpenManager

from src.auth.models import User


class DataBaseManager:
    """ Общий класс для CRUD """
    def __init__(self, model, parent_model, parent_name_id: str, use_user_id: bool = True):
        self.Model = model
        self.ParentModel = parent_model
        self.parent_name_id = parent_name_id
        self.use_user_id = use_user_id
        self.types_manager = TypeDataBaseManager(load_default_types=True)
        self.set_parent_type_database()

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
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar()

    async def get_entities(self, filter_value: int, user: User, session: AsyncSession):
        compare_attribute = getattr(self.Model, self.parent_name_id)
        query = select(self.Model).where(compare_attribute == filter_value)
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
