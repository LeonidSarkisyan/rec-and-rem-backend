from fastapi import APIRouter, Depends

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.depends import get_current_user


from profiles.schemas import ProfileCreate
from profiles.models import Profile

from profiles.services.db import ProfileDB


router = APIRouter(prefix='/profiles', tags=['Profile'])


@router.post('/')
async def create_profile(
        profile: ProfileCreate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ProfileDB.add_profile(profile, session, user)
