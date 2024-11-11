from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, EmailStr, HttpUrl


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


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


class UserGetWithPassword(UserGet):
    hashed_password: str


class UserGetWithProfile(UserGet):
    about: str
    social_links: list[HttpUrl]


class UserGetWithSubscriptions(UserGetWithProfile):
    subscribers: list[UserGet]
    subscribed: list[UserGet]


class Playlist(BaseSchema):
    user_id: UUID
    title: str
    private: bool = True
