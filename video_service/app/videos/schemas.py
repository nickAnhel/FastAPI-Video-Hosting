from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


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
