from contextlib import AbstractAsyncContextManager
from typing import Callable, Iterator, AsyncIterator, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, select

from src.database import Database, DATABASE_URL

from src.repositories.repositories_settings import RepositoriesSettings, abstract_settings


class BaseRepository:
    def __init__(
        self,
        settings: RepositoriesSettings,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession, None]]
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings

    async def get_all_entities(self):
        async with self._session_factory() as session:
            query = select(self._settings.model.real_model)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_ids_entities(self):
        async with self._session_factory() as session:
            query = select(self._settings.model.real_model.id)
            result = await session.execute(query)
            return result.mappings().all()

    async def get_entity_by_id(self, entity_id: int):
        async with self._session_factory() as session:
            query = select(self._settings.model.real_model).where(self._settings.model.real_model.id == entity_id)
            result = await session.execute(query)
            return result.scalar()

    async def get_entity_by_key(self, key: str, value):
        async with self._session_factory() as session:
            stmt = (
                select(self._settings.model.real_model)
                .where(self._settings.model.idents_fields.get_property(key) == value)
            )
            result = await session.execute(stmt)
            return result.scalar()

    async def add_entity(self, data: dict, return_result: bool = False):
        async with self._session_factory() as session:
            stmt = insert(self._settings.model.real_model).values(**data)
            await session.execute(stmt)
            await session.commit()
            return 'all good'

    async def add_many_entities(self, data: list):
        async with self._session_factory() as session:
            stmt = insert(self._settings.model.real_model).values(data)
            await session.execute(stmt)
            await session.commit()
            return 'roles was created'

    async def update_entity_by_id(self, entity_id: int, data: dict):
        async with self._session_factory() as session:
            stmt = (
                update(self._settings.model.real_model)
                .where(self._settings.model.real_model.id == entity_id)
                .values(**data)
            )
            await session.execute(stmt)
            await session.commit()
            return 'updated'

    async def delete_entity_by_id(self, entity_id: int):
        async with self._session_factory() as session:
            stmt = delete(self._settings.model.real_model).where(self._settings.model.real_model.id == entity_id)
            await session.execute(stmt)
            await session.commit()
            return 'deleted'

    async def delete_entities_by_id(self, entities_id: list[int]):
        async with self._session_factory() as session:
            stmt = (
                delete(self._settings.model.real_model)
                .where(self._settings.model.real_model.id.in_(entities_id))
            )
            print(stmt)
            await session.execute(stmt)
            await session.commit()
            return 'deleted'


abstract_repository = BaseRepository(abstract_settings, Database(DATABASE_URL))
