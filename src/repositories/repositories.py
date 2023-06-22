from contextlib import AbstractAsyncContextManager
from typing import Callable, Iterator, AsyncIterator, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, select

from src.database import Database, DATABASE_URL

from src.repositories.repositories_settings import RepositoriesSettings, abstract_settings


class BaseRepository:
    """ Репозиторий CRUD операций"""
    def __init__(
        self,
        settings: RepositoriesSettings,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    async def get_all_entities(self):
        async with self.session_factory() as session:
            query = select(self.settings.model.real_model)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_ids_entities(self):
        async with self.session_factory() as session:
            query = select(self.settings.model.real_model.id)
            result = await session.execute(query)
            return result.mappings().all()

    async def add_entity(self, data: dict):
        async with self.session_factory() as session:
            stmt = insert(self.settings.model.real_model).values(**data)
            await session.execute(stmt)
            await session.commit()
            return 'all good'

    async def add_many_entities(self, data: list):
        async with self.session_factory() as session:
            stmt = insert(self.settings.model.real_model).values(data)
            await session.execute(stmt)
            await session.commit()
            return 'roles was created'

    async def delete_entity_by_id(self, entity_id: int):
        async with self.session_factory() as session:
            stmt = delete(self.settings.model.real_model).where(self.settings.model.real_model.id == entity_id)
            await session.execute(stmt)
            await session.commit()
            return 'deleted'

    async def delete_entities_by_id(self, entities_id: list[int]):
        async with self.session_factory() as session:
            stmt = delete(self.settings.model.real_model.id).where(self.settings.model.real_model.id in entities_id)
            await session.execute(stmt)
            await session.commit()
            return 'deleted'


abstract_repository = BaseRepository(abstract_settings, Database(DATABASE_URL))
