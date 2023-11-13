from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.depends import get_query_search

from src.auth.depends import get_current_user

from src.workspace.depends import get_my_workspace

from src.folder.depends import get_my_folder
from src.folder.services.db import folder_database_manager
from src.folder.schemas import FolderCreate, FolderBase, FolderReadPublic, FolderWithAbstracts
from src.folder.service import FolderService


router = APIRouter(prefix='/workspace/{workspace_id}/folder', tags=['Folder'])
router_without_workspace_id = APIRouter(prefix='/workspace/folder', tags=['Folder'])


@router.post('/')
async def create_folder(
        folder: FolderCreate,
        workspace=Depends(get_my_workspace),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.add_entity(
        folder, workspace, user=user, session=session
    )


@router.get('/')
async def get_folders(
        workspace=Depends(get_my_workspace),
        search_query: str = Depends(get_query_search),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.get_entities(
        filter_value=workspace.id, user=user, session=session, search_query=search_query
    )


@router_without_workspace_id.get('/copy/{folder_id}', response_model=FolderWithAbstracts)
async def copy_abstracts_from_open_folder(
        folder_open_url: str,
        folder=Depends(get_my_folder),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.copy_child_entities_from_url_open(
        entity_id=folder.id,
        entity_url_open=folder_open_url,
        user=user,
        session=session
    )

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
    return await folder_database_manager.update_entity_by_id(folder, entity_id=folder_id, user=user, session=session)


@router_without_workspace_id.delete('/{folder_id}')
async def delete_folder(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.delete_entity_by_id(folder_id, user, session)

# Эндпоинты для открытия / закрытия папок другими пользователями


@router_without_workspace_id.post('/opening/{folder_id}')
async def open_or_close_public_folder(
        folder_id: int,
        is_open: bool,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.open_or_close_entity_by_id(
        folder_id, user, session, is_open=is_open, count_symbols=12
    )


@router_without_workspace_id.get('/opening/show/{folder_id}')
async def get_unique_url(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await folder_database_manager.get_unique_url(folder_id, user, session, count_symbols=12)


@router_without_workspace_id.get('/opening/{folder_open_url}', response_model=FolderReadPublic)
async def get_public_folder(
    folder_open_url: str,
    workspace_id: int = 0,
    user=Depends(get_current_user),
):
    return await FolderService.copy_opened_entity_by_id(folder_open_url, user, parent_id=workspace_id)
