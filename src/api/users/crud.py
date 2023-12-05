from fastapi import HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from core.hash_password import get_password_hash, verify_password

from api.users.schemas import CreateUser, User
from core import models


async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(models.User).where(models.User.username == username)
    result = await db.execute(stmt)
    user = result.scalars().first()
    await db.commit()
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(models.User).where(models.User.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    await db.commit()
    return user


async def create_user(db: AsyncSession, user: CreateUser):
    hashed_password = get_password_hash(user.password)
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
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def is_admin(db: AsyncSession, admin: User):
    stmt1 = select(models.User).filter(models.User.username == admin.username)
    result = await db.execute(stmt1)
    administrator = result.scalars().first()
    return administrator.is_admin


async def assign_admin(db: AsyncSession, admin: User, username: str):
    if not await is_admin(db, admin):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admins can assign other admins ;)'
        )
    user = await get_user_by_username(db, username)
    if not user:
        return None
    stmt2 = (
        update(models.User)
        .where(models.User.username == username)
        .values(is_admin=True)
    )
    await db.execute(stmt2)
    await db.commit()
    await db.refresh(user)
    return user
