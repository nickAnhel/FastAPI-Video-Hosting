from typing import Literal
from uuid import UUID
from sqlalchemy.exc import IntegrityError, DBAPIError

from app.config import settings
from app.videos.repository import VideoRepository
from app.videos.schemas import VideoCreate, VideoGet
from app.videos.external import upload_file_to_s3, delete_files_from_s3, delete_all_video_comments
from app.videos.models import VideoModel
from app.videos.enums import VideoOrder
from app.videos.exceptions import (
    VideoNotFound,
    VideoTitleAlreadyExists,
    VideoDataWrongFormat,
    PermissionDenied,
    CantUploadVideoToS3,
    CantUploadPreviewToS3,
    CantDeleteVideoFromS3,
    CantDeleteComments,
)


class VideoService:
    def __init__(self, repository: VideoRepository):
        self._repository = repository

    async def create_video(
        self,
        video: bytes,
        preview: bytes,
        data: VideoCreate,
    ) -> VideoGet:
        try:
            video_model: VideoModel = await self._repository.create(data=data.model_dump())
        except IntegrityError as exc:
            raise VideoTitleAlreadyExists(f"Video with title {data.title} already exists") from exc
        except DBAPIError as exc:
            raise VideoDataWrongFormat("Title or description is too long") from exc

        await self._upload_video_files(
            video=video,
            preview=preview,
            video_model=video_model,
        )

        return VideoGet.model_validate(video_model)

    async def _upload_video_files(
        self,
        video: bytes,
        preview: bytes,
        video_model: VideoModel,
    ) -> None:
        if not await upload_file_to_s3(file=video, filename=settings.file_prefixes.video + str(video_model.id)):
            await self._repository.delete(id=video_model.id)
            raise CantUploadVideoToS3()

        if not await upload_file_to_s3(
            file=preview, filename=settings.file_prefixes.preview + str(video_model.id)
        ):
            await self._repository.delete(id=video_model.id)
            raise CantUploadPreviewToS3()

    async def search_videos(
        self,
        query: str,
    ) -> list[VideoGet]:
        videos = await self._repository.search(search_query=query)
        return [VideoGet.model_validate(video) for video in videos]

    async def get_video(
        self,
        **filters,
    ) -> VideoGet:
        video = await self._repository.get_single(**filters)
        await self._increment(column="views", id=video.id)  # type: ignore
        return self._check_video_exists(video)

    async def get_videos(
        self,
        order: VideoOrder = VideoOrder.ID,  # type: ignore
        offset: int = 0,
        limit: int = 100,
        user_id: UUID | None = None,
    ) -> list[VideoGet]:
        params = {"order": order, "offset": offset, "limit": limit}
        if user_id:
            params["user_id"] = user_id

        videos = await self._repository.get_multi(**params)
        return [VideoGet.model_validate(video) for video in videos]

    async def delete_video(
        self,
        token: str,
        id: UUID,
        user_id: UUID,
    ) -> None:
        video = await self._repository.get_single(id=id)
        self._check_video_exists(video)

        if not video.user_id == user_id:  # type: ignore
            raise PermissionDenied(f"User with id {user_id} can't delete video with id {id}.")

        if not await delete_files_from_s3(
            filenames=[
                settings.file_prefixes.video + str(id),
                settings.file_prefixes.preview + str(id),
            ]
        ):
            raise CantDeleteVideoFromS3()

        if not await delete_all_video_comments(video_id=id, token=token):
            raise CantDeleteComments()

        await self._repository.delete(id=id)

    async def delete_videos(
        self,
        token: str,
        user_id: UUID,
    ) -> int:
        videos = await self.get_videos(user_id=user_id)

        if not await delete_files_from_s3(
            filenames=[settings.file_prefixes.video + str(video.id) for video in videos]
            + [settings.file_prefixes.preview + str(video.id) for video in videos]
        ):
            raise CantDeleteVideoFromS3()

        for video in videos:
            if not await delete_all_video_comments(video_id=video.id, token=token):
                raise CantDeleteComments(f"Can't delete comments for video with id {video.id}.")

        return await self._repository.delete(user_id=user_id)

    async def _increment(
        self,
        column: Literal["views", "likes", "dislikes"],
        id: UUID,
    ) -> VideoGet:
        video = await self._repository.increment(column=column, id=id)
        return self._check_video_exists(video)

    async def _decrement(
        self,
        column: Literal["views", "likes", "dislikes"],
        id: UUID,
    ) -> VideoGet:
        video = await self._repository.decrement(column=column, id=id)
        return self._check_video_exists(video)

    async def increment_likes(self, id: UUID) -> VideoGet:
        return await self._increment(column="likes", id=id)

    async def decrement_likes(self, id: UUID) -> VideoGet:
        return await self._decrement(column="likes", id=id)

    async def increment_dislikes(self, id: UUID) -> VideoGet:
        return await self._increment(column="dislikes", id=id)

    async def decrement_dislikes(self, id: UUID) -> VideoGet:
        return await self._decrement(column="dislikes", id=id)

    def _check_video_exists(self, video: VideoModel | None) -> VideoGet:
        if not video:
            raise VideoNotFound()

        return VideoGet.model_validate(video)
