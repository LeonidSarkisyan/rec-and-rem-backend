from fastapi import APIRouter, Depends

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.profiles.schemas import ProfileCreate, ProfileUpdate
from src.profiles.models import Profile

from src.profiles.services.db import ProfileDB


router = APIRouter(prefix='/profiles', tags=['Profile'])


@router.post('/')
async def create_profile(
        profile: ProfileCreate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ProfileDB.add_profile(profile, session, user)


@router.get('/')
async def get_my_profile(
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ProfileDB.get_my_profile(session, user)


@router.patch('/')
async def update_profile(
        profile: ProfileUpdate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ProfileDB.update_profile(profile, session, user)
