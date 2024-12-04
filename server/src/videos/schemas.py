from uuid import UUID
from datetime import datetime
from pydantic import Field

from src.schemas import BaseSchema


class VideoCreate(BaseSchema):
    title: str = Field(max_length=50)
    description: str = Field(max_length=255)
    user_id: UUID


class VideoGet(VideoCreate):
    id: UUID
    views: int
    likes: int
    dislikes: int
    created_at: datetime


class VideoLikesDislikes(BaseSchema):
    id: UUID
    likes: int = Field(ge=0)
    dislikes: int = Field(ge=0)
