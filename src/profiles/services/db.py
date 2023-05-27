from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
from fastapi import status

from auth.models import User

from profiles.schemas import ProfileCreate
from profiles.models import Profile

from profiles.exceptions.http import ProfileAlreadyExist


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
