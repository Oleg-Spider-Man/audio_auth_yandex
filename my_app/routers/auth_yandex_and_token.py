import uuid
from urllib.parse import urlencode
from fastapi import APIRouter, Request, Depends, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse
from my_app import schemas
from my_app.auth_.create_token import cr_token
from my_app.auth_.verification_token import verify_token
from my_app.config import YANDEX_CLIENT_ID, YANDEX_REDIRECT_URI
from my_app.dependencies import get_async_session
from my_app.operations.crud import create_user, get_user
from my_app.operations.utils import exchange_code_token, get_user_data

router = APIRouter(
    prefix="/auth_and_token",
    tags=["auth"]
)


@router.get("/auth/yandex/login", response_model=schemas.YandexLogin)
async def yandex_login():
    try:
        state = str(uuid.uuid4())
        auth_url = "https://oauth.yandex.ru/authorize"
        params = {
            "response_type": "code",
            "client_id": YANDEX_CLIENT_ID,
            "redirect_uri": YANDEX_REDIRECT_URI,
            "state": state
        }
        query_string = urlencode(params)
        redirect_url = f"{auth_url}?{query_string}"
        return {"redirect_url": redirect_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/yandex/callback", response_model=str)
async def yandex_callback(request: Request, db: AsyncSession = Depends(get_async_session)):
    try:
        code = request.query_params.get("code")
        if code:
            # Обмен кода на токен

            token_data = await exchange_code_token(code)

            # Получение данных пользователя

            user_data = await get_user_data(token_data)

            # Создание токена для вашего приложения
            openid = user_data.get("default_email")
            name = user_data.get("real_name")
            # здесь функция крид добавления пользователя в свою бд после яндекса
            existing_user = await get_user(openid, db)
            if not existing_user:
                await create_user(openid, name, db)
            token = await cr_token(openid)
            return token

        else:
            return JSONResponse({"error": "Код авторизации не получен"}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token/refresh", response_model=str)
async def refresh_token(user_id: str = Depends(verify_token)):
    try:
        return await cr_token(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
