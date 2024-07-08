from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class BaseChema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseChema):
    username: str
    email: EmailStr
    password: str


class UserGet(BaseChema):
    id: UUID
    username: str
    email: EmailStr


class UserGetWithPassword(UserGet):
    hashed_password: str