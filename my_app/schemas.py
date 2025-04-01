from pydantic import BaseModel


class YandexLogin(BaseModel):
    redirect_url: str


class User(BaseModel):
    email: str
    name: str
    role: str


class UserUpdate(BaseModel):
    role: str


class AudioFileResponse(BaseModel):
    filename: str
    path: str
