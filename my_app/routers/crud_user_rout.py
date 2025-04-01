from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from my_app import schemas
from my_app.auth_.verification_token import get_current_user
from my_app.dependencies import get_async_session
from my_app.operations.crud import get_user, update_user, delete_user

router = APIRouter(
    prefix="/crud_user",
    tags=["user"]
)


@router.get("/read_user/{email}", response_model=schemas.User)
async def read_user(email: str, openid: str = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    try:
        user_data = await get_user(email, db)
        if user_data is None:
            raise HTTPException(status_code=404, detail=f"Hello {openid}, User data not found")
        return user_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/put_user/{email}", response_model=schemas.User)
async def put_user(email: str, new_data: schemas.UserUpdate,
                   openid: str = Depends(get_current_user),
                   db: AsyncSession = Depends(get_async_session)):
    try:
        await update_user(email, openid, new_data, db)
        return await get_user(email, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_user/{email}", response_model=dict)
async def delete_us(email: str, openid: str = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    try:
        return await delete_user(email, openid, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
