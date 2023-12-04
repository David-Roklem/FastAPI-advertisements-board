from fastapi import HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from core.hash_password import get_password_hash, verify_password

from api.users.schemas import CreateUser
from core import models


async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(models.User).where(models.User.username == username)
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


async def appoint_admin(db: AsyncSession, admin: str, username: str):

    # Check if a user who's trying to appoint and admin is an admin himself
    stmt1 = select(models.User).filter(models.User.username == admin)
    result = await db.execute(stmt1)
    administrator = result.scalars().first()
    if administrator.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only chosen ones can appoint admins, you are not them ;)'
        )

    # Update is_admin field in DB
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
