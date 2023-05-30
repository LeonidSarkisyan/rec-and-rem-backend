from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.auth.depends import get_current_user

from src.profiles.schemas import ProfileCreate, ProfileUpdate
from src.profiles.models import Profile


from src.profiles.services.db import ProfileDB, AvatarDB
from src.profiles.services.files import create_unique_filename


from src.profiles.services.s3 import get_avatar_from_s3
from src.profiles.depends import get_current_profile


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
        profile: Profile = Depends(get_current_profile)
):
    return profile


@router.patch('/')
async def update_profile(
        profile: ProfileUpdate,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ProfileDB.update_profile(profile, session, user)


# API endpoints for avatar

@router.post('/avatar')
async def upload_avatar_profile(
        file: UploadFile = File(),
        user=Depends(get_current_profile),
        session: AsyncSession = Depends(get_async_session)
):
    url = create_unique_filename(file)
    return await AvatarDB.upload_file(file, url, session, user)


@router.get('/avatar')
async def get_avatar_profile(profile=Depends(get_current_profile), session: AsyncSession = Depends(get_async_session)):
    avatar = await AvatarDB.get_url_file(session, profile)
    avatar_file = get_avatar_from_s3(avatar.url)
    return StreamingResponse(avatar_file['Body'])


@router.put('/avatar')
async def update_upload_avatar_profile(
        file: UploadFile = File(),
        user=Depends(get_current_profile),
        session: AsyncSession = Depends(get_async_session)
):
    url = create_unique_filename(file)
    return await AvatarDB.update_upload_file(file, url, session, user)
