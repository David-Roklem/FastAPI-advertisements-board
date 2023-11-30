from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User
from .advertisement import Ad


class Review(Base):
    text: Mapped[str] = mapped_column(String(250))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))

    user: Mapped['User'] = relationship(back_populates='reviews')
    ads: Mapped['Ad'] = relationship(back_populates='reviews')
