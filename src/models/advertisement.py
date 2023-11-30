from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User
from .comment import Comment
from .complaint import Complaint
from .review import Review


class Ad(Base):

    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str]
    type: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='ads')
    comments: Mapped[list['Comment']] = relationship(
        back_populates='ads',
    )
    complaints: Mapped[list['Complaint']] = relationship(
        back_populates='ads',
    )
    reviews: Mapped[list['Review']] = relationship(
        back_populates='ads',
    )
