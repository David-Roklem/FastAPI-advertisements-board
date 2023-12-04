from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.ads.schemas import AdBase, AdTitle, CreateAd
from api.ads import crud
from auth.jwt_auth import get_current_user
from core.db import get_async_session
from api.users.schemas import UserToken

router = APIRouter(prefix='/ads', tags=['Ads'])


@router.post('/create-ad/')
async def create_ad(
    ad: CreateAd,
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    db_ad = await crud.publish_ad(db, ad, current_user)
    return db_ad


@router.get('/your-ads/')
async def show_current_user_ads(
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    user_ads = await crud.get_current_user_ads(db, current_user)
    return user_ads


@router.get('/all-ads/', response_model=list[AdTitle])
async def show_all_ads(
    db: AsyncSession = Depends(get_async_session)
):
    all_ads = await crud.get_all_ads(db)
    return all_ads
