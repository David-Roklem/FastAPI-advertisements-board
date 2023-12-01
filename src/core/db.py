from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)

from src.core.config import settings

async_engine = create_async_engine(
    settings.db_url_asyncpg, future=True, echo=True
)
async_session_maker = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
