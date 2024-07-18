from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseSchema):
    content: str
    user_id: UUID
    video_id: UUID


class CommentGet(CommentCreate):
    id: UUID
    likes: int
    dislikes: int
    created_at: datetime
