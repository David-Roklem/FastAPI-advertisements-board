from uuid import uuid4

from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)
from sqlalchemy.dialects.postgresql import UUID


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
