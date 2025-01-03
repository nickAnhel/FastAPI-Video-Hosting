import io
from typing import Literal
from uuid import UUID
from sqlalchemy.exc import IntegrityError, DBAPIError
from PIL import Image

from src.config import settings
from src.exceptions import PermissionDenied

from src.s3_storage.utils import upload_file, delete_files
from src.s3_storage.exceptions import CantUploadFileToStorage, CantDeleteFileFromStorage
from src.users.schemas import UserGet

from src.videos.repository import VideoRepository
from src.videos.schemas import VideoCreate, VideoGet, VideoLikesDislikes, VideoViews, VideoGetWithUserStatus
from src.videos.models import VideoModel
from src.videos.enums import VideoOrder, HistoryOrder, LikedOrder
from src.videos.exceptions import VideoNotFound, VideoTitleAlreadyExists, VideoDataWrongFormat, CantReactVideo


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
            filename=settings.file_prefixes.preview + str(video_model.id) + ".jpg",
        ):
            await self._repository.delete(video_id=video_model.id)
            raise CantUploadFileToStorage("Failed to upload preview")

        if not await upload_file(
            file=video,
            filename=settings.file_prefixes.video + str(video_model.id),
        ):
            await delete_files(filenames=[settings.file_prefixes.preview + str(video_model.id)])
            await self._repository.delete(video_id=video_model.id)
            raise CantUploadFileToStorage("Failed to upload video file")

    async def search_videos(
        self,
        query: str,
        order: VideoOrder = VideoOrder.ID,  # type: ignore
        offset: int = 0,
        desc: bool = False,
        limit: int = 100,
    ) -> list[VideoGet]:
        videos = await self._repository.search(
            search_query=query,
            offset=offset,
            limit=limit,
        )
        return [VideoGet.model_validate(video) for video in videos]

    async def get_video(
        self,
        user: UserGet | None = None,
        **filters,
    ) -> VideoGet | VideoGetWithUserStatus:
        video = await self._repository.get_single(**filters)
        video = self._check_video_exists(video)

        if user:
            is_liked = await self._repository.is_liked(user_id=user.id, video_id=video.id)
            is_disliked = await self._repository.is_disliked(user_id=user.id, video_id=video.id)

            try:
                await self._repository.add_to_watch_history(
                    user_id=user.id,
                    video_id=video.id,
                )
            except IntegrityError:
                pass

            return VideoGetWithUserStatus(
                **video.model_dump(),
                is_liked=is_liked,
                is_disliked=is_disliked,
            )

        return video

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

        await self._repository.delete(video_id=id)

    async def delete_user_videos(
        self,
        user_id: UUID,
    ) -> None:
        videos = await self._repository.get_multi(user_id=user_id)
        filenames = []

        for v in videos:
            filenames.append(settings.file_prefixes.video + str(v.id))
            filenames.append(settings.file_prefixes.preview + str(v.id))

        await delete_files(filenames)
        await self._repository.delete_multi(user_id=user_id)

    async def get_watch_history(
        self,
        user_id: UUID,
        order: HistoryOrder = HistoryOrder.WATCHED_AT,  # type: ignore
        offset: int = 0,
        desc: bool = False,
        limit: int = 100,
    ) -> list[VideoGet]:
        video_models = await self._repository.get_watch_history(
            order=order,
            order_desc=desc,
            offset=offset,
            limit=limit,
            user_id=user_id,
        )
        return [VideoGet.model_validate(v) for v in video_models]

    async def remove_video_from_watch_history(
        self,
        user_id: UUID,
        video_id: UUID,
    ) -> None:
        await self._repository.remove_from_watch_history(
            user_id=user_id,
            video_id=video_id,
        )

    async def clear_watch_history(
        self,
        user_id: UUID,
    ) -> None:
        await self._repository.clear_history(user_id=user_id)

    async def get_liked_videos(
        self,
        user_id: UUID,
        order: LikedOrder = LikedOrder.LIKED_AT,  # type: ignore
        offset: int = 0,
        desc: bool = False,
        limit: int = 100,
    ) -> list[VideoGet]:
        video_models = await self._repository.get_liked(
            order=order, order_desc=desc, offset=offset, limit=limit, user_id=user_id
        )
        return [VideoGet.model_validate(v) for v in video_models]

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

    async def increment_views(
        self,
        video_id: UUID,
    ) -> VideoViews:
        await self._increment("views", id=video_id)
        return await self.get_views(video_id=video_id)

    async def like_video(
        self,
        video_id: UUID,
        user_id: UUID,
    ) -> VideoLikesDislikes:
        try:
            await self._repository.like(user_id=user_id, video_id=video_id)
        except IntegrityError as exc:
            raise CantReactVideo("Can't like video twice") from exc

        await self._repository.increment("likes", id=video_id)
        await self.undislike_video(video_id=video_id, user_id=user_id)
        likes, dislikes, _ = await self._repository.get_stats(id=video_id)
        return VideoLikesDislikes(
            id=video_id,
            likes=likes,
            dislikes=dislikes,
        )

    async def get_views(
        self,
        video_id: UUID,
    ) -> VideoViews:
        _, _, views = await self._repository.get_stats(id=video_id)
        return VideoViews(
            id=video_id,
            views=views,
        )

    async def unlike_video(
        self,
        video_id: UUID,
        user_id: UUID,
    ) -> VideoLikesDislikes:
        if await self._repository.unlike(user_id=user_id, video_id=video_id) == 1:
            await self._repository.decrement("likes", id=video_id)

        likes, dislikes, _ = await self._repository.get_stats(id=video_id)
        return VideoLikesDislikes(
            id=video_id,
            likes=likes,
            dislikes=dislikes,
        )

    async def dislike_video(
        self,
        video_id: UUID,
        user_id: UUID,
    ) -> VideoLikesDislikes:
        try:
            await self._repository.dislike(user_id=user_id, video_id=video_id)
        except IntegrityError as exc:
            raise CantReactVideo("Can't dislike video twice") from exc

        await self._repository.increment("dislikes", id=video_id)
        await self.unlike_video(video_id=video_id, user_id=user_id)
        likes, dislikes, _ = await self._repository.get_stats(id=video_id)
        return VideoLikesDislikes(
            id=video_id,
            likes=likes,
            dislikes=dislikes,
        )

    async def undislike_video(
        self,
        video_id: UUID,
        user_id: UUID,
    ) -> VideoLikesDislikes:
        if await self._repository.undislike(user_id=user_id, video_id=video_id) == 1:
            await self._repository.decrement("dislikes", id=video_id)

        likes, dislikes, _ = await self._repository.get_stats(id=video_id)
        return VideoLikesDislikes(
            id=video_id,
            likes=likes,
            dislikes=dislikes,
        )

    async def get_subscriptions(
        self,
        user_id: UUID,
        order: VideoOrder = VideoOrder.ID,  # type: ignore
        offset: int = 0,
        desc: bool = False,
        limit: int = 100,
    ) -> list[VideoGet]:
        videos = await self._repository.get_subscriptions(
            user_id=user_id,
            order=order,
            order_desc=desc,
            offset=offset,
            limit=limit,
        )

        return [VideoGet.model_validate(video) for video in videos]

    async def get_playlist_videos(
        self,
        playlist_id: UUID,
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoGet]:
        videos = await self._repository.get_playlist_videos(
            playlist_id=playlist_id,
            offset=offset,
            limit=limit,
        )
        return [VideoGet.model_validate(video) for video in videos]

    def _check_video_exists(self, video: VideoModel | None) -> VideoGet:
        if not video:
            raise VideoNotFound()

        return VideoGet.model_validate(video)
