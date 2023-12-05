from pydantic import UUID4, BaseModel


class CommentBase(BaseModel):
    text: str


class CreateComment(CommentBase):
    message: str


class Comment(BaseModel):
    user_id: UUID4
    ad_id: UUID4
