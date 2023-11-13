from sqlalchemy import select, insert, delete, update

from sqlalchemy.exc import DBAPIError, IntegrityError

from src.database import async_session_maker
from src.services.databasemanager.sqlquerymaker import BaseSQLMaker
from src.exceptions.http import NotFound, AccessDenied, OwnEntity, NotValidCode, ErrorByCreating

from src.auth.models import User


class BaseDAO:
    model = None
    parent_id = None
    parent_name_id: str = None
    search_fields = None
    have_user: bool = None
    only_owner: bool = None
    sql_maker: BaseSQLMaker
    child_model = None
    child_parent_id = None
    child_name_parent_id: str = None

    @classmethod
    async def get_entity_by_filters(cls, *filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter(*filters)
            result = await session.execute(query)
            entity = result.scalar()
            return entity

    @classmethod
    async def get_entity_by_id(cls, entity_id: int):
        async with async_session_maker() as session:
            query = cls.sql_maker.select(entity_id)
            result = await session.execute(query)
            entity = result.scalar()
            return entity

    @classmethod
    async def get_children_by_id(cls, entity_id: int):
        async with async_session_maker() as session:
            query_child = select(cls.child_model).where(cls.child_parent_id == entity_id)
            result_children = await session.execute(query_child)
            children = result_children.scalars().all()
            return children

    @classmethod
    async def create(cls, data_dict: dict, returning=None):
        async with async_session_maker() as session:
            if not returning:
                returning = cls.model.id
            stmt = cls.sql_maker.insert(data_dict, returning)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def create_children(cls, objects: list):
        async with async_session_maker() as session:
            result = await session.execute(insert(cls.child_model).returning(cls.child_model), objects)
            await session.commit()
            return result.scalars().all()

    @classmethod
    async def mark_as_delete_entity(cls, mark_deleted: bool, *filters):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .returning(cls.model)
                .filter(*filters)
                .values(is_deleted=mark_deleted)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, update_data: dict, *filters):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .returning(cls.model)
                .filter(*filters)
                .values(**update_data)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()


class BaseDAOService(BaseDAO):

    @classmethod
    async def get_entity_by_id(cls, entity_id: int):
        try:
            result = await super().get_entity_by_id(entity_id)
        except DBAPIError:
            raise NotValidCode
        else:
            return result

    @classmethod
    async def create_or_update_by_id(cls, update_data: dict, *filters):
        try:
            result = await cls.create(update_data)
        except IntegrityError:
            result = await cls.update(update_data, *filters)
        return result
