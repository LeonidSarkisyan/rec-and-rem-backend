from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.depends import get_query_search

from src.auth.depends import get_current_user

from src.workspace.models import Workspace
from src.workspace.schemas import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate

from src.workspace.services.db import WorkspaceDB

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
