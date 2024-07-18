from uuid import UUID
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, PositiveInt


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VideoCreate(BaseSchema):
    title: str
    description: str
    user_id: UUID


class VideoGet(VideoCreate):
    id: UUID
    user_id: UUID
    views: PositiveInt | Literal[0]
    likes: PositiveInt | Literal[0]
    dislikes: PositiveInt | Literal[0]
    created_at: datetime
