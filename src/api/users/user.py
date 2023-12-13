from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.users import crud
from api.users.schemas import CreateUser
from auth.jwt_auth import create_access_token, get_current_user
from auth.token_schemas import Token
from core.db import get_async_session
from api.users.schemas import UserToken
from core.config import settings

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/sign-up/', status_code=201)
async def create_user(
    user: CreateUser, db: AsyncSession = Depends(get_async_session)
):
    db_user = await crud.get_user_by_username(db, username=user.username)
    db_email = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with such a username already registered'
        )
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with such an email already registered'
        )
    return await crud.create_user(db=db, user=user)


@router.post('/token/', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session)
):
    user = await crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me/', response_model=UserToken)
async def read_users_me(
    current_user: Annotated[UserToken, Depends(get_current_user)]
):
    return current_user


@router.patch('/appoint-admin/')
async def appoint_admin(
    current_user: Annotated[UserToken, Depends(get_current_user)],
    username: str,
    db: AsyncSession = Depends(get_async_session)
):
    user = await crud.assign_admin(db, admin=current_user, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid username or password'
        )
    return {
        'message': f'{username} has been appointed as administrator'
    }
