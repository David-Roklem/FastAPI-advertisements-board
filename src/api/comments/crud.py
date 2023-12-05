from fastapi import HTTPException, status

from sqlalchemy import UUID, select
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


async def remove_comment_by_admin(
        db: AsyncSession,
        comment_id: UUID
):
    stmt = select(models.Comment).where(models.Comment.id == comment_id)
    result = await db.execute(stmt)
    db_comment = result.scalars().first()
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no comment with such an id in database'
        )
    comment_text = db_comment.text
    await db.delete(db_comment)
    await db.commit()
    return comment_text
