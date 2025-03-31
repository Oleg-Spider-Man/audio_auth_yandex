import uuid
from urllib.parse import urlencode

import uvicorn
from fastapi import FastAPI, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from starlette.responses import JSONResponse, RedirectResponse
from my_app.auth_.create_token import cr_token
from my_app.auth_.verification_token import get_current_user, security
from my_app.config import YANDEX_CLIENT_ID, YANDEX_REDIRECT_URI
from my_app.dependencies import get_async_session
from my_app.operations.crud import create_user, get_user, create_sup_user
from my_app.operations.utils import exchange_code_token, get_user_data

app = FastAPI()
# await расставить
# ошибки ловить и в роутер засунуть. и каждый обзац в функцию
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/auth/yandex/login")
async def yandex_login():
    state = str(uuid.uuid4())
    auth_url = "https://oauth.yandex.ru/authorize"
    params = {
        "response_type": "code",
        "client_id": YANDEX_CLIENT_ID,
        "redirect_uri": YANDEX_REDIRECT_URI,
        #"scope": "login:email login:name",
        "state": state
    }
    query_string = urlencode(params)
    redirect_url = f"{auth_url}?{query_string}"
    return {"redirect_url": redirect_url}
    #return RedirectResponse(redirect_url, status_code=302)



@app.get("/auth/yandex/callback")
async def yandex_callback(request: Request, db: AsyncSession = Depends(get_async_session)):
    code = request.query_params.get("code")
    if code:
        # # Обмен кода на токен
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
        a = await cr_token(openid)
        return a

    else:
        return JSONResponse({"error": "Код авторизации не получен"}, status_code=400)


#в крид схемы валидации добавить
# в описании про использования алембика напомнить
#создание супер пользователя эндпоинт в крид сделать функцию
@app.post("/create_superuser")
async def create_superuser(email: str, name: str, db: AsyncSession = Depends(get_async_session)):
    existing_user = get_user(email, db)
    if existing_user:
        return {"error": "Пользователь уже существует"}
    await create_sup_user(email, name, db)
    return {"message": "Суперпользователь создан"}


# здесь логику аудио
@app.get("/api/profile")
async def read_profile(user_id: str = Depends(get_current_user)):#token: str = Depends(security)):
    #await get_current_user(token)
    #return {"email": await get_current_user(token)}
    return {"email": user_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)






