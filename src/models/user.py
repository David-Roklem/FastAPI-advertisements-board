from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .advertisement import Ad
from .comment import Comment
from .complaint import Complaint
from .review import Review


class User(Base):

    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        String(50), unique=True
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    ads: Mapped[list['Ad']] = relationship(
        back_populates='user',
    )
    comments: Mapped[list['Comment']] = relationship(
        back_populates='user',
    )
    complaints: Mapped[list['Complaint']] = relationship(
        back_populates='user',
    )
    reviews: Mapped[list['Review']] = relationship(
        back_populates='user',
    )
