from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, UploadFile

from src.auth.models import User

from src.profiles.schemas import ProfileCreate, ProfileUpdate
from src.profiles.models import Profile, Avatar

from src.profiles.services.s3 import upload_avatar_to_s3

from src.profiles.exceptions.http import ProfileAlreadyExist


class ProfileDB:

    @staticmethod
    async def add_profile(profile: ProfileCreate, session: AsyncSession, user: User):
        try:
            stmt = insert(Profile).values(
                first_name=profile.first_name,
                second_name=profile.second_name,
                username=profile.username,
                user_id=user.id
            )
            await session.execute(stmt)
            await session.commit()
        except IntegrityError:
            raise ProfileAlreadyExist
        return 'success'

    @staticmethod
    async def update_profile(profile: ProfileUpdate, session: AsyncSession, user: User):
        data = {key: value for key, value in profile.dict().items() if value}
        stmt = update(Profile).where(Profile.user_id == user.id).values(**data)
        await session.execute(stmt)
        await session.commit()
        return 'success'

    @staticmethod
    async def get_my_profile(session: AsyncSession, user: User):
        query = select(Profile).where(Profile.user_id == user.id)
        result = await session.execute(query)
        return result.scalar()


class AvatarDB:

    @staticmethod
    async def get_url_file(session: AsyncSession, profile: Profile) -> Avatar:
        query = select(Avatar).where(Avatar.profile_id == profile.id)
        result = await session.execute(query)
        return result.scalar()

    @staticmethod
    async def upload_file(file: UploadFile, url: str, session: AsyncSession, profile: Profile):
        stmt = insert(Avatar).values(url=url, profile_id=profile.id)
        await session.execute(stmt)
        await session.commit()
        upload_avatar_to_s3(file, url)
        return 'success'

    @staticmethod
    async def update_upload_file(file: UploadFile, url: str, session: AsyncSession, profile: Profile):
        stmt = update(Avatar).where(Avatar.profile_id == profile.id).values(url=url)
        await session.execute(stmt)
        await session.commit()
        upload_avatar_to_s3(file, url)
        return 'update'
