from typing import Literal
from uuid import UUID

from app.videos.repository import VideoRepository
from app.videos.scemas import VideoCreate, VideoGet
from app.videos.exceptions import VideoNotFound, CantUploadVideoToS3, CantDeleteVideoFromS3
from app.videos.utils import upload_file_to_s3, delete_file_from_s3
from app.videos.models import VideoModel


class VideoService:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    async def create_video(
        self,
        file: bytes,
        data: VideoCreate,
    ) -> VideoGet:
        video_model = await self.repository.create(data=data.model_dump())

        if not await upload_file_to_s3(file=file, filename=str(video_model.id)):
            await self.delete_video(id=video_model.id)  # type: ignore
            raise CantUploadVideoToS3()

        return VideoGet.model_validate(video_model)

    async def get_video(
        self,
        **filters,
    ) -> VideoGet:
        video = await self.repository.get_single(**filters)
        return self._validate_video_exists(video)

    async def get_videos(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoGet]:
        videos = await self.repository.get_multi(order=order, offset=offset, limit=limit)
        return [VideoGet.model_validate(video) for video in videos]

    async def delete_video(
        self,
        id: UUID,
    ) -> None:
        if not await delete_file_from_s3(filename=str(id)):
            raise CantDeleteVideoFromS3()

        await self.repository.delete(id=id)

    async def _increment(
        self,
        column: Literal["views", "likes", "dislikes"],
        id: UUID,
    ) -> VideoGet:
        video = await self.repository.increment(column=column, id=id)
        return self._validate_video_exists(video)

    async def _decrement(
        self,
        column: Literal["views", "likes", "dislikes"],
        id: UUID,
    ) -> VideoGet:
        video = await self.repository.increment(column=column, id=id)
        return self._validate_video_exists(video)

    async def increment_views(self, id: UUID) -> VideoGet:
        return await self._increment(column="views", id=id)

    async def increment_likes(self, id: UUID) -> VideoGet:
        return await self._increment(column="likes", id=id)

    async def decrement_likes(self, id: UUID) -> VideoGet:
        return await self._decrement(column="likes", id=id)

    async def increment_dislikes(self, id: UUID) -> VideoGet:
        return await self._increment(column="dislikes", id=id)

    async def decrement_dislikes(self, id: UUID) -> VideoGet:
        return await self._decrement(column="likes", id=id)

    def _validate_video_exists(self, video: VideoModel | None) -> VideoGet:
        if not video:
            raise VideoNotFound()
        return VideoGet.model_validate(video)
