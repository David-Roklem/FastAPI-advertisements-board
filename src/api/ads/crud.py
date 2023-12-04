from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.schemas import User

from api.ads.schemas import Ad
from core import models


async def publish_ad(
        db: AsyncSession,
        ad: Ad,
        current_user: User
):
    current_user_id = current_user.id
    db_ad = models.Ad(
        title=ad.title,
        description=ad.description,
        type=ad.type,
        user_id=current_user_id
    )
    db.add(db_ad)
    await db.commit()
    await db.refresh(db_ad)
    return db_ad


async def get_current_user_ads(
        db: AsyncSession,
        current_user: User
):
    current_user_id = current_user.id
    stmt = select(models.Ad).filter(models.Ad.user_id == current_user_id)
    result = await db.execute(stmt)
    ads = result.scalars().all()
    if not ads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You don\'t have any published ads'
        )
    return ads


async def get_all_ads(
        db: AsyncSession,
):
    stmt = select(models.Ad)
    result = await db.execute(stmt)
    ads = result.scalars().all()
    if not ads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no ads published yet. Be the one who starts it!'
        )
    return ads


async def get_ad_in_details(db: AsyncSession, ad_number: int):
    stmt = select(models.Ad).where(models.Ad.ad_number == ad_number)
    result = await db.execute(stmt)
    ad = result.scalars().first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no such an ad under this ad number'
        )
    return ad
