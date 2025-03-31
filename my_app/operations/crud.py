from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from my_app import models
from my_app.models import User


async def get_user(openid: str, db: AsyncSession):
    query = select(models.User).filter(models.User.email == openid)
    result = await db.execute(query)
    return result.scalar()


async def create_user(openid: str, name: str, db: AsyncSession):
    new_user = User(email=openid, name=name, role="user")
    db.add(new_user)
    return await db.commit()


async def create_sup_user(openid: str, name: str, db: AsyncSession):
    new_user = User(email=openid, name=name, role="superuser")
    db.add(new_user)
    return await db.commit()
