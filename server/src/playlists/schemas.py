from typing import Any, Self
from uuid import UUID
from pydantic import Field

from src.schemas import BaseSchema


class PlaylistCreate(BaseSchema):
    title: str = Field(max_length=50)
    description: str = Field(max_length=255)
    private: bool = False


class PlaylistGet(BaseSchema):
    id: UUID
    user_id: UUID
    title: str
    description: str
    private: bool = False
    videos_count: int


class Video(BaseSchema):
    id: UUID
    title: str


class PlaylistGetWithFirstVideo(PlaylistGet):
    videos: list[Video] = Field(default_factory=list)

    @classmethod
    def model_validate(
        cls, obj: Any, *, strict: bool | None = None, from_attributes: bool | None = None, context: Any | None = None
    ) -> Self:
        if obj.videos:
            obj.videos = [obj.videos[-1]]
        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)
