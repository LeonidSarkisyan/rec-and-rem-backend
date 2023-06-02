from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

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


folder_db_manager = FolderDataBaseManager()
