from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    name: str
    role: str


class UserUpdateSchema(BaseModel):
    name: str | None = None
    role: str | None = None
