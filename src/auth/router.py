from datetime import timedelta

from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from config import AuthConfig
from database import get_async_session

from auth.schemas import UserCreate, UserLogin

from auth.services.auth import UserAuth, create_access_token
from auth.services.db import UserDB

from auth.depends import get_current_user

router = APIRouter(tags=['Account'], prefix='/account')


@router.post('/register')
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    id_new_user = await UserDB.add_user(user, session)
    return {'status': 'Ok', 'user_id': id_new_user}


@router.get('/me')
async def get_my_account(cookie=Depends(get_current_user)):
    return cookie


@router.post('/login')
async def login(
        user_login: UserLogin,
        response: Response,
        session: AsyncSession = Depends(get_async_session)
):
    user = await UserAuth.authenticate_user(user_login.email, user_login.password, session)
    access_token_expires = timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(key="Authorization", value=f"{access_token}",
                        httponly=True)
    return {'status': 'Ok'}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('Authorization')
    return {'status': 'Ok'}
