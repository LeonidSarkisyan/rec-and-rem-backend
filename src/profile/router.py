from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from schemas import ProfileCreate

router = APIRouter(prefix='/profile', tags=['Profile'])


@router.post('/')
async def create_profile(profile: ProfileCreate, session: AsyncSession = Depends(get_async_session)):
    return profile
