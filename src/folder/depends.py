from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.folder.services.db import folder_database_manager


async def get_my_folder(
        folder_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    folder = await folder_database_manager.get_entity_by_id(folder_id, user, session)
    return folder
