from uuid import UUID
from pydantic import Field, EmailStr, HttpUrl

from src.schemas import BaseSchema


class UserCreate(BaseSchema):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    about: str = Field(max_length=255)
    social_links: list[HttpUrl]


class UserGet(BaseSchema):
    id: UUID
    username: str
    email: EmailStr
    subscribers_count: int = Field(ge=0)
    is_subscribed: bool | None = None


class UserGetWithPassword(UserGet):
    hashed_password: str


class UserGetWithProfile(UserGet):
    about: str
    social_links: list[HttpUrl]


class UserGetWithSubscriptions(UserGetWithProfile):
    subscribers: list[UserGet]
    subscribed: list[UserGet]


class UserUpdate(BaseSchema):
    username: str | None = Field(max_length=50, default=None)
    about: str | None = Field(max_length=255, default=None)
    social_links: list[HttpUrl] | None = None
