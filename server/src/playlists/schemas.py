from uuid import UUID

from pydantic import Field

# from pydantic import field_validator

from src.schemas import BaseSchema
from src.videos.schemas import VideoGet


class PlaylistCreate(BaseSchema):
    title: str
    description: str
    private: bool = False

    # @field_validator("title")
    # @classmethod
    # def validate_title(cls, v):
    #     if v in ["Watch History", "Liked Videos", "Disliked Videos"]:
    #         raise ValueError("Playlist title cannot be named Watch History, Liked Videos or Disliked Videos")
    #     return v


class PlaylistGet(BaseSchema):
    id: UUID
    user_id: UUID
    title: str
    description: str
    private: bool = False


class PlaylistGetWithVideos(PlaylistGet):
    videos: list[VideoGet] = Field(default_factory=list)
