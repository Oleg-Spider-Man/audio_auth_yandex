from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from my_app import models, schemas
from my_app.models import User, AudioFile


async def get_user(openid: str, db: AsyncSession):
    query = select(models.User).filter(models.User.email == openid)
    result = await db.execute(query)
    return result.scalar()


async def get_audio_user(user_email: str, db: AsyncSession):
    query = (select(AudioFile).filter(AudioFile.user_email == user_email))
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(openid: str, name: str, db: AsyncSession):
    new_user = User(email=openid, name=name, role="user")
    db.add(new_user)
    return await db.commit()


async def update_user(email: str, openid: str, new_data: schemas.UserUpdate, db: AsyncSession):
    user = await get_user(openid, db)
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Только суперюзеры могут изменять пользователей")
    query = update(models.User).where(models.User.email == email).values(**new_data.dict())
    await db.execute(query)
    await db.commit()
    return {"message": "Данные пользователя обновлены"}


async def create_sup_user(openid: str, name: str, db: AsyncSession):
    new_user = User(email=openid, name=name, role="superuser")
    db.add(new_user)
    return await db.commit()


async def delete_user(email: str, openid: str, db: AsyncSession):
    user = await get_user(openid, db)
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Только суперюзеры могут удалять пользователей")
    query = delete(models.User).where(models.User.email == email)
    await db.execute(query)
    await db.commit()
    return {"message": "Пользователь удален"}
