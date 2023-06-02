from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.workspace.depends import get_my_workspace

from src.folder.services.db import folder_db_manager

from src.folder.schemas import FolderCreate, FolderBase

router = APIRouter(prefix='/workspace/{workspace_id}/folder', tags=['Folder'])


# Создать CRUD folder
@router.post('/')
async def create_folder(
        folder: FolderCreate,
        workspace=Depends(get_my_workspace),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.add_folder(folder, workspace, user, session)


@router.get('/')
async def get_folders(
        workspace=Depends(get_my_workspace),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.get_folders(workspace, user, session)


@router.get('/{folder_id}')
async def get_folder(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.get_folder_by_id(folder_id, user, session)


@router.patch('/{folder_id}')
async def update_folder(
        folder_id: int,
        folder: FolderCreate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.update_folder(folder_id, folder, user, session)


@router.delete('/{folder_id}')
async def delete_folder(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.delete_folder(folder_id, user, session)

