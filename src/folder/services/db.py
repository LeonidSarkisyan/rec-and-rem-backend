from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.services.opening import OpenManager

from src.auth.models import User

from src.workspace.models import Workspace

from src.folder.schemas import FolderCreate, FolderUpdate
from src.folder.models import Folder


class FolderDataBaseManager:
    @staticmethod
    async def add_folder(folder: FolderCreate, workspace: Workspace, user: User, session: AsyncSession):
        stmt = insert(Folder).returning(Folder.id).values(
            title=folder.title, workspace_id=workspace.id, user_id=user.id)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar()

    @staticmethod
    async def get_folders(workspace: Workspace, user: User, session: AsyncSession):
        query = select(Folder).where(Folder.workspace_id == workspace.id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_folder_by_id(folder_id: int, user: User, session: AsyncSession):
        query = select(Folder).where(Folder.id == folder_id)
        result = await session.execute(query)
        folder = result.scalar()
        if folder.user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        return folder

    @staticmethod
    async def update_folder(folder_id: int, folder: FolderUpdate, user: User, session: AsyncSession):
        stmt = update(Folder).returning(Folder.user_id).where(Folder.id == folder_id).values(title=folder.title)
        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return 'success'

    @staticmethod
    async def delete_folder(folder_id: int, user: User, session: AsyncSession):
        stmt = delete(Folder).returning(Folder.user_id).where(Folder.id == folder_id)
        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return 'success'

    @staticmethod
    async def open_or_close_folder_by_id(
            folder_id: int,
            user: User,
            session: AsyncSession,
            is_open: bool,
    ):

        unique_url: str = await OpenManager.create_open_url(folder_id) if is_open else ''

        data = {
            "url_open": unique_url,
            "is_open": is_open
        }

        stmt = update(Folder)\
            .where(Folder.id == folder_id)\
            .values(**data)\
            .returning(Folder.user_id)

        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return {'status': 'Ok'}

    @staticmethod
    async def get_public_folder_by_id(folder_open_url: str, user: User, session: AsyncSession):
        folder_id = await OpenManager.get_entity_id(folder_open_url)
        query = select(Folder).where(Folder.id == folder_id)
        result = await session.execute(query)
        folder = result.scalar()
        if not folder:
            raise HTTPException(status_code=404, detail='Не найдено')
        if not folder.is_open:
            raise HTTPException(status_code=404, detail='Не найдено')
        return folder


folder_db_manager = FolderDataBaseManager()
