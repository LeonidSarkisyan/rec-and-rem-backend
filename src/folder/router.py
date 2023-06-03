from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.workspace.depends import get_my_workspace

from src.folder.services.db import folder_db_manager, folder_database_manager

from src.folder.schemas import FolderCreate, FolderBase, FolderReadPublic

router = APIRouter(prefix='/workspace/{workspace_id}/folder', tags=['Folder'])
router_without_workspace_id = APIRouter(prefix='/workspace/folder', tags=['Folder'])


@router.post('/')
async def create_folder(
        folder: FolderCreate,
        workspace=Depends(get_my_workspace),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.add_entity(folder, workspace, user=user, session=session)


@router.get('/')
async def get_folders(
        workspace=Depends(get_my_workspace),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.get_entities(workspace.id, user, session)

# router_without_workspace_id


@router_without_workspace_id.get('/{folder_id}')
async def get_folder(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.get_entity_by_id(folder_id, user, session)


@router_without_workspace_id.patch('/{folder_id}')
async def update_folder(
        folder_id: int,
        folder: FolderCreate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.update_folder(folder_id, folder, user, session)


@router_without_workspace_id.delete('/{folder_id}')
async def delete_folder(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.delete_folder(folder_id, user, session)

# Эндпоинты для открытия / закрытия папок другими пользователями


@router_without_workspace_id.post('/opening/{folder_id}')
async def open_or_close_public_folder(
        folder_id: int,
        is_open: bool,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.open_or_close_folder_by_id(folder_id, user, session, is_open=is_open)


@router_without_workspace_id.get('/opening/{folder_open_url}', response_model=FolderReadPublic)
async def get_public_folder(
    folder_open_url: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await folder_db_manager.get_public_folder_by_id(folder_open_url, user, session)
