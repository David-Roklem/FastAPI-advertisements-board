from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import BigInteger, func
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
    )

    def __repr__(self) -> str:
        '''Representation of a string object.

        Returns:
            object: string object
        '''
        return self.__class__.__name__

    __str__ = __repr__


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
        back_populates='user'
    )
    comments: Mapped[list['Comment']] = relationship(
        back_populates='user'
    )
    complaints: Mapped[list['Complaint']] = relationship(
        back_populates='user'
    )
    reviews: Mapped[list['Review']] = relationship(
        back_populates='user'
    )


class Ad(Base):

    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str]
    type: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # ad_number: Mapped[int] = mapped_column(
    #     BigInteger,
    #     Sequence('ad_number_seq', start=55555),
    #     server_default='ad_number_seq',
    #     nullable=False,
    #     unique=True,
    #     index=True,
    # )
    ad_number: Mapped[int] = mapped_column(
        BigInteger,
        default=func.abs(func.random() * 1000000),
        unique=True,
        index=True
    )

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


class Comment(Base):
    text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))

    user: Mapped['User'] = relationship(back_populates='comments')
    ads: Mapped['Ad'] = relationship(back_populates='comments')


class Complaint(Base):
    text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))

    user: Mapped['User'] = relationship(back_populates='complaints')
    ads: Mapped['Ad'] = relationship(back_populates='complaints')


class Review(Base):
    text: Mapped[str] = mapped_column(String(250))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ad_id: Mapped[int] = mapped_column(ForeignKey('ads.id'))

    user: Mapped['User'] = relationship(back_populates='reviews')
    ads: Mapped['Ad'] = relationship(back_populates='reviews')
