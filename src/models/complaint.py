from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .advertisement import Ad
from .user import User


class Complaint(Base):
    text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))

    user: Mapped['User'] = relationship(back_populates='complaints')
    ads: Mapped['Ad'] = relationship(back_populates='complaints')
