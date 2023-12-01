from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings

async_engine = create_async_engine(
    settings.db_url_asyncpg, future=True, echo=True
)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session
