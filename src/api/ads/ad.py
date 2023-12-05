from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.ads.schemas import AdBase, AdTitle, CreateAd, AdDelete
from api.ads import crud
from auth.jwt_auth import get_current_user
from core.db import get_async_session
from api.users.schemas import UserToken

router = APIRouter(prefix='/ads', tags=['Ads'])


@router.post('/create-ad/', response_model=AdBase)
async def create_ad(
    ad: CreateAd,
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    db_ad = await crud.publish_ad(db, ad, current_user)
    return db_ad


@router.get(
        '/all-your-ads/',
        response_model=list[AdTitle],
        description='Options for "type_" field: "sell", "rent", "give away"'
)
async def show_all_current_user_ads(
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    type_: str = None,
):
    user_ads = await crud.get_current_user_ads(
        type_,
        page,
        page_size,
        db,
        current_user
    )
    return user_ads


@router.get(
        '/all-ads/',
        response_model=list[AdTitle],
        description='Options for "type_" field: "sell", "rent", "give away"'
)
async def show_all_ads(
    type_: str = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    db: AsyncSession = Depends(get_async_session)
):
    all_ads = await crud.get_all_ads(type_, page, page_size, db)
    return all_ads


@router.get('/ad-lookup/', response_model=AdTitle)
async def show_ad_in_details(
    ad_number: int,
    db: AsyncSession = Depends(get_async_session),
):
    all_ads = await crud.get_ad_in_details(db, ad_number)
    return all_ads


@router.delete('/delete-ad/', response_model=AdDelete)
async def delete_ad(
    ad_number: int,
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    deleted_ad = await crud.remove_ad(db, ad_number, current_user)
    return AdDelete(
        message='The ad successfully deleted',
        title=deleted_ad.title,
        ad_number=deleted_ad.ad_number
    )
