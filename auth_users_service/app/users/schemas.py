from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, EmailStr, HttpUrl


class BaseChema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseChema):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    about: str = Field(max_length=255)
    social_links: list[HttpUrl]


class UserGet(BaseChema):
    id: UUID
    username: str
    email: EmailStr


class UserGetWithPassword(UserGet):
    hashed_password: str


class UserGetWithProfile(UserGet):
    about: str
    social_links: list[HttpUrl]


class UserGetWithSubscriptions(UserGetWithProfile):
    subscribers: list[UserGet]
    subscribed: list[UserGet]
