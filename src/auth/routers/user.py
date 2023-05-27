from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.models import User
from auth.schemas import UserRead

from auth.services.db import UserDB

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/', response_model=List[UserRead])
async def get_users(query_search: str = None, session: AsyncSession = Depends(get_async_session)):
    return await UserDB.get_users(query_search, session)
