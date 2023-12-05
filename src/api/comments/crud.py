from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.ads.crud import get_ad_in_details
from api.comments.schemas import CommentBase
from api.users.schemas import User

from api.ads.schemas import Ad
from core import models


# Additional functionality
async def publish_comment(
        db: AsyncSession,
        comment: CommentBase,
        ad_number: int,
        current_user: User
):
    current_user_id = current_user.id
    db_ad = await get_ad_in_details(db, ad_number)
    ad_id = db_ad.id
    db_comment = models.Comment(
        text=comment,
        user_id=current_user_id,
        ad_id=ad_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment
