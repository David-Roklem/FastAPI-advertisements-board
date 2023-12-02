from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.users import crud
from api.users.schemas import CreateUser
from core.db import get_async_session

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/')
async def create_user(
    user: CreateUser, db: AsyncSession = Depends(get_async_session)
):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )
    return await crud.create_user(db=db, user=user)


@router.get('/login/')
async def login(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_async_session)
):
    user = await crud.authenticate_user(
        db, username=username, password=password
    )
    if not user:
        raise HTTPException(
            status_code=401, detail='Invalid username or password'

        )
    return {'access_token': user.id, 'token_type': 'bearer'}
