import io
from typing import Literal
from uuid import UUID
from sqlalchemy.exc import IntegrityError, DBAPIError
from PIL import Image

from src.config import settings
from src.exceptions import PermissionDenied

from src.s3_storage.utils import upload_file, delete_files
from src.s3_storage.exceptions import CantUploadFileToStorage, CantDeleteFileFromStorage

from src.videos.repository import VideoRepository
from src.videos.schemas import VideoCreate, VideoGet
from src.videos.models import VideoModel
from src.videos.enums import VideoOrder
from src.videos.exceptions import (
    VideoNotFound,
    VideoTitleAlreadyExists,
    VideoDataWrongFormat,
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
        img = Image.open(preview)
        img.thumbnail((1280, 720))
        img_bytes = io.BytesIO()
        img.save(img_bytes, "PNG")
        img_bytes = img_bytes.getvalue()

        if not await upload_file(
            file=img_bytes,
            filename=settings.file_prefixes.preview + str(video_model.id),
        ):
            await self._repository.delete(id=video_model.id)
            raise CantUploadFileToStorage("Failed to upload preview")

        if not await upload_file(
            file=video,
            filename=settings.file_prefixes.video + str(video_model.id),
        ):
            await delete_files(filenames=[settings.file_prefixes.preview + str(video_model.id)])
            await self._repository.delete(id=video_model.id)
            raise CantUploadFileToStorage("Failed to upload video file")

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
        desc: bool = False,
        limit: int = 100,
        user_id: UUID | None = None,
    ) -> list[VideoGet]:
        params = {"order": order, "offset": offset, "limit": limit, "order_desc": desc}
        if user_id:
            params["user_id"] = user_id

        videos = await self._repository.get_multi(**params)
        return [VideoGet.model_validate(video) for video in videos]

    async def delete_video(
        self,
        id: UUID,
        user_id: UUID,
    ) -> None:
        video = await self._repository.get_single(id=id)
        self._check_video_exists(video)

        if not video.user_id == user_id:  # type: ignore
            raise PermissionDenied(f"User with id {user_id} can't delete video with id {id}.")

        if not await delete_files(
            filenames=[
                settings.file_prefixes.video + str(id),
                settings.file_prefixes.preview + str(id),
            ]
        ):
            raise CantDeleteFileFromStorage("Failed to delete files from storage")

        await self._repository.delete(id=id)

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
