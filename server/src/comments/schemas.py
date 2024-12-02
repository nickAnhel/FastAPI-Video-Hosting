from uuid import UUID
from datetime import datetime
from pydantic import Field

from src.schemas import BaseSchema


class CommentCreate(BaseSchema):
    content: str = Field(max_length=255)
    video_id: UUID


class CommentGet(CommentCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
