from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PlaylistCreate(BaseSchema):
    title: str
    description: str
    video_ids: list[UUID]
    private: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v in ["Watch History", "Liked Videos", "Disliked Videos"]:
            raise ValueError("Playlist title cannot be named Watch History, Liked Videos or Disliked Videos")
        return v


class PlaylistGet(BaseSchema):
    id: UUID
    user_id: UUID
    title: str
    description: str
    video_ids: list[UUID]
    private: bool = False
