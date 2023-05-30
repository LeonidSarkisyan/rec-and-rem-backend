from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.depends import get_current_user
from src.auth.models import User

from src.profiles.services.db import ProfileDB


async def get_current_profile(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ProfileDB.get_my_profile(session, user)
