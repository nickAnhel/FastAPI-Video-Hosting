from uuid import UUID
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, PositiveInt


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VideoCreate(BaseSchema):
    title: str
    description: str


class VideoGet(VideoCreate):
    id: UUID
    views: PositiveInt | Literal[0]
    likes: PositiveInt | Literal[0]
    dislikes: PositiveInt | Literal[0]
    created_at: datetime
