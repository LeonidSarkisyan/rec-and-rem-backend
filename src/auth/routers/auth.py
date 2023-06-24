from datetime import timedelta

from fastapi import APIRouter, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.config import AuthConfig
from src.database import get_async_session

from src.auth.schemas import UserCreate, UserLogin, UserRead, ChangePassword

from src.auth.models import User

from src.auth.services.auth import UserAuth, create_access_token
from src.auth.services.db import UserDB

from src.auth.depends import get_current_user
from src.auth.services.permissions import Permission, get_valid_moderator, get_valid_user, get_valid_admin

router = APIRouter(tags=['Account'], prefix='/account')


@router.post('/register')
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    id_new_user = await UserDB.add_user(user, session)
    return {'status': 'Ok', 'user_id': id_new_user}


@router.get('/me', response_model=UserRead)
async def get_my_account(user: User = Depends(get_current_user)):
    return user


@router.post('/login', status_code=204)
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
    response.set_cookie(key="Authorization", value=f"{access_token}", httponly=True)


@router.post('/logout', status_code=204)
async def logout(response: Response):
    response.delete_cookie('Authorization')


@router.post('/password', status_code=204)
async def change_password(
        password: ChangePassword,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(get_current_user)
):
    await UserAuth.change_password(password, session, user)


# ПРИМЕР ИСПОЛЬЗОВАНИЯ КАСТОМНОГО ПЕРМИШОНА
# @router.get('/moderator')
# async def moderator(user: Permission = Depends(user_permission)):
#     return 'success'
