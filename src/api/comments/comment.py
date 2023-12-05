from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.comments.schemas import Comment, CreateComment
from api.comments import crud
from auth.jwt_auth import get_current_user
from core.db import get_async_session
from api.users.schemas import UserToken

router = APIRouter(prefix='/comments', tags=['Comments'])


# Additional functionality
@router.post('/create-comment/', response_model=CreateComment)
async def create_comment(
    comment: str,
    ad_number: int,
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    db_comment = await crud.publish_comment(
        db,
        comment,
        ad_number,
        current_user
    )
    return CreateComment(
        text=db_comment.text,
        message='Your comment was successfully published@'
    )
