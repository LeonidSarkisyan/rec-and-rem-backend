from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.auth.models import User

from src.workspace.schemas import WorkspaceRead, WorkspaceCreate, WorkspaceUpdate
from src.workspace.models import Workspace

from src.workspace.services.opening import WorkspaceOpenManager


class WorkspaceDB:
    @staticmethod
    async def add_workspace(workspace: WorkspaceCreate, user: User, session: AsyncSession):
        stmt = insert(Workspace).returning(Workspace.id).values(
            title=workspace.title, description=workspace.description, user_id=user.id
        )
        result = await session.execute(stmt)
        new_workspace = result.mappings().first()
        await session.commit()
        return new_workspace

    @staticmethod
    async def get_workspace(query_search: str, user: User, session: AsyncSession):
        if query_search:
            query = select(Workspace).where(
                Workspace.user_id == user.id
            ) .where(
                Workspace.title.ilike('%' + query_search + '%')
            )
        else:
            query = select(Workspace).where(Workspace.user_id == user.id)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_workspace_by_id(workspace_id: int, user: User, session: AsyncSession) -> Workspace:
        query = select(Workspace).where(Workspace.id == workspace_id)
        result = await session.execute(query)
        workspace = result.scalar()
        if not workspace:
            raise HTTPException(status_code=404, detail='Не найдено')
        if workspace.user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        return workspace

    @staticmethod
    async def update_workspace_by_id(
            workspace_id: int,
            workspace_update: WorkspaceUpdate,
            user: User,
            session: AsyncSession
    ):
        stmt = update(Workspace)\
            .where(Workspace.id == workspace_id)\
            .values(**workspace_update.dict())\
            .returning(Workspace.user_id)

        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return {'status': 'Ok'}

    @staticmethod
    async def get_public_workspace_by_id(workspace_open_url: str, user: User, session: AsyncSession):
        workspace_id = await WorkspaceOpenManager.get_workspace_id(workspace_open_url)
        query = select(Workspace).where(Workspace.id == workspace_id)
        result = await session.execute(query)
        workspace = result.scalar()
        if not workspace:
            raise HTTPException(status_code=404, detail='Не найдено')
        if not workspace.is_open:
            raise HTTPException(status_code=404, detail='Не найдено')
        return workspace

    @staticmethod
    async def open_or_close_workspace_by_id(
            workspace_id: int,
            user: User,
            session: AsyncSession,
            is_open: bool,
    ):

        unique_url = await WorkspaceOpenManager.create_open_url(workspace_id) if is_open else ''

        data = {
            "url_open": unique_url,
            "is_open": is_open
        }

        stmt = update(Workspace)\
            .where(Workspace.id == workspace_id)\
            .values(**data)\
            .returning(Workspace.user_id)

        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return {'status': 'Ok'}

    @staticmethod
    async def delete_workspace_by_id(
            workspace_id: int,
            user: User,
            session: AsyncSession
    ):
        stmt = delete(Workspace).where(Workspace.id == workspace_id).returning(Workspace.user_id)
        result = await session.execute(stmt)
        user_id = result.scalar()
        if user_id != user.id:
            raise HTTPException(status_code=403, detail='Недоступно')
        else:
            await session.commit()
        return {'status': 'Ok'}


