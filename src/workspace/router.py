from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.depends import get_query_search

from src.auth.depends import get_current_user

from src.workspace.models import Workspace
from src.workspace.schemas import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate, WorkspaceReadPublic

from src.workspace.services.db import WorkspaceDB

from src.folder.router import router as folder_router


router = APIRouter(prefix='/workspace', tags=['Workspace'])


@router.post('/')
async def create_workspace(
        workspace: WorkspaceCreate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.add_workspace(workspace, user, session)


@router.get('/', response_model=List[WorkspaceRead])
async def get_workspace_list(
        query_search: str = Depends(get_query_search),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.get_workspace(query_search, user, session)


@router.get('/{workspace_id}')
async def get_workspace(
        workspace_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.get_workspace_by_id(workspace_id, user, session)


@router.patch('/{workspace_id}')
async def update_workspace(
        workspace_id: int,
        workspace: WorkspaceUpdate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.update_workspace_by_id(workspace_id, workspace, user, session)


@router.delete('/{workspace_id}')
async def delete_workspace(
        workspace_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.delete_workspace_by_id(workspace_id, user, session)


# Эндпоинты для открытия / закрытия рабочего пространства другим пользователям

@router.post('/opening/{workspace_id}')
async def open_or_close_public_workspace(
        workspace_id: int,
        is_open: bool,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.open_or_close_workspace_by_id(workspace_id, user, session, is_open=is_open)


@router.get('/opening/{workspace_open_url}', response_model=WorkspaceReadPublic)
async def get_public_workspace(
    workspace_open_url: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await WorkspaceDB.get_public_workspace_by_id(workspace_open_url, user, session)
