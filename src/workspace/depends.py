from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.workspace.services.db import WorkspaceDB


async def get_my_workspace(
        workspace_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    workspace = await WorkspaceDB.get_workspace_by_id(workspace_id, user, session)
    return workspace
