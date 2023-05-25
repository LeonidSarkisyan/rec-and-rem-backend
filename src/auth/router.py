from fastapi import APIRouter, Depends

from sqlalchemy import insert, select

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.schemas import UserCreate
from auth.models import User
from auth.exceptions.http import EmailAlreadyExists

from auth.services import UserDB

router = APIRouter(tags=['Account'], prefix='/account')


@router.post('/')
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    id_new_user = await UserDB.add_user(user, session)
    return {'status': 'Ok', 'user_id': id_new_user}
