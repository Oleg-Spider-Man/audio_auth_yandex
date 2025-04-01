import uvicorn
from fastapi import FastAPI
from my_app.routers import crud_user_rout, audio_rout, auth_yandex_and_token

app = FastAPI()

# в описании про использования алембика напомнить


app.include_router(auth_yandex_and_token.router)
app.include_router(audio_rout.router)
app.include_router(crud_user_rout.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)






