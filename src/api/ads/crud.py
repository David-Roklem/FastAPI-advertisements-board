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
