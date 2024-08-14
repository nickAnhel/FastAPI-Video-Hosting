from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PlaylistCreate(BaseSchema):
    title: str
    description: str
    video_ids: list[UUID]
    private: bool = False


class PlaylistGet(PlaylistCreate):
    id: UUID
    user_id: UUID
