from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.comments.schemas import Comment, CommentResponse
from api.comments import crud as comments_crud
from api.users import crud as users_crud
from auth.jwt_auth import get_current_user
from core import models
from core.db import get_async_session
from api.users.schemas import UserToken

router = APIRouter(prefix='/comments', tags=['Comments'])


# Additional functionality
@router.post('/create-comment/', response_model=CommentResponse)
async def create_comment(
    comment: str,
    ad_number: int,
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    db_comment = await comments_crud.publish_comment(
        db,
        comment,
        ad_number,
        current_user
    )
    return CommentResponse(
        message='Your comment was successfully published',
        text=db_comment.text
    )


@router.post('/delete-comment/', response_model=CommentResponse)
async def delete_comment_by_admin(
    comment_id: UUID4,
    current_user: Annotated[UserToken, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    if users_crud.is_admin(db, current_user):
        comment_text = await comments_crud.remove_comment_by_admin(
            db, comment_id
        )
        return CommentResponse(
            message='The comment was successfully deleted',
            text=comment_text
        )
