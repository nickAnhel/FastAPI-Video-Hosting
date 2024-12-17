from uuid import UUID
from datetime import datetime

from src.schemas import BaseSchema


class Video(BaseSchema):
    id: UUID
    title: str


class Channel(BaseSchema):
    id: UUID
    username: str


class NotificationGet(BaseSchema):
    id: UUID
    user_id: UUID
    is_read: bool
    created_at: datetime

    video: Video
    channel: Channel
