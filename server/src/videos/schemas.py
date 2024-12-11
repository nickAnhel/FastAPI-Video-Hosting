from uuid import UUID
from datetime import datetime
from pydantic import Field

from src.schemas import BaseSchema


class VideoCreate(BaseSchema):
    title: str = Field(max_length=50)
    description: str = Field(max_length=255)
    user_id: UUID


class VideoAuthor(BaseSchema):
    id: UUID
    username: str
    subscribers_count: int


class VideoGet(VideoCreate):
    id: UUID
    views: int
    likes: int
    dislikes: int
    created_at: datetime
    user: VideoAuthor


class VideoLikesDislikes(BaseSchema):
    id: UUID
    likes: int = Field(ge=0)
    dislikes: int = Field(ge=0)


class VideoViews(BaseSchema):
    id: UUID
    views: int


class VideoGetWithUserStatus(VideoGet):
    is_liked: bool
    is_disliked: bool
