import datetime
from typing import List

from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.folder.depends import get_my_folder
from src.folder.models import Folder

from src.abstract.schemas import AbstractCreate, AbstractRead, AbstractUpdate, AbstractContent
from src.abstract.services.db import abstract_database_manager
from src.abstract.service import AbstractService


router = APIRouter(prefix='/folder/{folder_id}/abstract', tags=['Abstract'])


@router.post('/')
async def create_abstract(
        abstract: AbstractCreate,
        folder: Folder = Depends(get_my_folder),
        user=Depends(get_current_user),
):
    return await AbstractService.create(abstract, folder, user)


@router.get('/', response_model=List[AbstractRead])
async def get_abstracts(
        folder: Folder = Depends(get_my_folder),
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.get_entities(filter_value=folder.id, user=user, session=session)


router_without_folder_id = APIRouter(prefix='/folder/abstract', tags=['Abstract'])


@router_without_folder_id.get('/{abstract_id}', response_model=AbstractRead)
async def get_abstract(
        abstract_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.get_entity_by_id(abstract_id, user, session)


@router_without_folder_id.get('/{abstract_id}/content')
async def get_content_abstract(
        abstract_id: int,
        user=Depends(get_current_user),
):
    return await AbstractService.get_content(abstract_id, user)


@router_without_folder_id.post('/{abstract_id}/content')
async def set_content_abstract(
        abstract_id: int,
        content: AbstractContent,
        user=Depends(get_current_user)
):
    return await AbstractService.set_content(content.content, abstract_id, user)


@router_without_folder_id.patch('/{abstract_id}')
async def update_abstract(
        abstract_id: int,
        abstract: AbstractUpdate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.update_entity_by_id(
        abstract, entity_id=abstract_id, user=user, session=session
    )


@router_without_folder_id.delete('/{abstract_id}')
async def delete_abstract(
        abstract_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.delete_entity_by_id(abstract_id, user, session)


@router_without_folder_id.delete('/mark/{abstract_id}', status_code=204)
async def mark_as_delete_abstract(
        abstract_id: int,
        mark_deleted: bool,
        user=Depends(get_current_user)
):
    return await AbstractService.mark_as_delete_entity(abstract_id, mark_deleted, user)


@router_without_folder_id.delete('/{abstract_id}')
async def delete_abstract(
        abstract_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.delete_entity_by_id(abstract_id, user, session)


@router_without_folder_id.post('/opening/{abstract_id}')
async def open_or_close_public_abstract(
        abstract_id: int,
        is_open: bool,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.open_or_close_entity_by_id(
        abstract_id, user, session, is_open, count_symbols=14
    )


@router_without_folder_id.get('/opening/show/{abstract_id}')
async def get_unique_url(
        abstract_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await abstract_database_manager.get_unique_url(abstract_id, user, session, count_symbols=14)


@router_without_folder_id.get('/opening/{abstract_url_open}')
async def get_public_abstract(
        abstract_url_open: str,
        folder_id: int,
        user=Depends(get_current_user),
):
    return await AbstractService.copy_opened_entity_by_id(abstract_url_open, user, folder_id)




