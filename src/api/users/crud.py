from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.hash_password import get_password_hash, verify_password

from api.users.schemas import CreateUser
from core import models


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).filter(models.User.username == username)
    )
    return result.scalars().first()


async def create_user(db: AsyncSession, user: CreateUser):
    hashed_password = get_password_hash(user.password)
    print(hashed_password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    print(user)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
