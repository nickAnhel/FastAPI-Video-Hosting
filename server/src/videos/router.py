from typing import Annotated
from uuid import UUID
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    BackgroundTasks,
    Query,
    Depends,
    Form,
    status,
)

from src.schemas import Status

from src.auth.dependencies import get_current_user, get_current_optional_user, get_current_user_with_subscriptions
from src.users.schemas import UserGet, UserGetWithSubscriptions
from src.playlists.dependencies import get_playlists_service
from src.playlists.service import PlaylistService
from src.notifications.dependencies import get_notifications_service
from src.notifications.service import NotificationsService

from src.videos.schemas import VideoGet, VideoCreate, VideoLikesDislikes, VideoViews, VideoGetWithUserStatus
from src.videos.service import VideoService
from src.videos.dependencies import get_video_service
from src.videos.enums import VideoOrder, HistoryOrder, LikedOrder


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.post("/")
async def create_video(
    video: UploadFile,
    preview: UploadFile,
    bt: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    user: UserGetWithSubscriptions = Depends(get_current_user_with_subscriptions),
    video_service: VideoService = Depends(get_video_service),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> VideoGet:
    if video.content_type != "video/mp4":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only mp4 files are allowed for videos",
        )

    if preview.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only jpeg or png files are allowed for previews",
        )

    data = VideoCreate(title=title, description=description, user_id=user.id)

    created_video = await video_service.create_video(
        video=video.file,  # type: ignore
        preview=preview.file,  # type: ignore
        data=data,
    )

    bt.add_task(notifications_service.send_notification_to_user_subs, user=user, video=created_video)
    # await notifications_service.send_notification_to_user_subs(user=user, video=created_video)

    return created_video


@router.get("/search")
async def search_videos(
    query: Annotated[str, Query(max_length=50)],
    offset: int = 0,
    limit: int = 100,
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.search_videos(
        query=query,
        offset=offset,
        limit=limit,
    )


@router.get("/list")
async def get_videos(
    order: VideoOrder = VideoOrder.ID,  # type: ignore
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user_id: UUID | None = None,
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_videos(
        user_id=user_id,
        order=order,
        desc=desc,
        offset=offset,
        limit=limit,
    )


@router.get("/")
async def get_video_by_id(
    video_id: UUID,
    user: UserGet | None = Depends(get_current_optional_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet | VideoGetWithUserStatus:
    return await video_service.get_video(
        user=user,
        id=video_id,
    )


@router.delete("/")
async def delete_video_by_id(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> Status:

    await video_service.delete_video(
        id=video_id,
        user_id=user.id,
    )
    return Status(detail="Video deleted successfully")


@router.patch("/add-view")
async def add_view_to_video(
    video_id: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoViews:
    return await video_service.increment_views(video_id=video_id)


@router.get("/history")
async def get_watch_history(
    order: HistoryOrder = HistoryOrder.WATCHED_AT,  # type: ignore
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_watch_history(
        user_id=user.id,
        order=order,
        desc=desc,
        limit=limit,
        offset=offset,
    )


@router.patch("/history/remove")
async def remove_video_from_watch_history(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> Status:
    await video_service.remove_video_from_watch_history(
        user_id=user.id,
        video_id=video_id,
    )
    return Status(detail="Video successfully removed from watch history")


@router.delete("/history/clear")
async def clear_watch_history(
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> Status:
    await video_service.clear_watch_history(
        user_id=user.id,
    )
    return Status(detail="Watch history successfully cleared")


@router.get("/liked")
async def get_liked_videos(
    order: LikedOrder = LikedOrder.LIKED_AT,  # type: ignore
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_liked_videos(
        user_id=user.id,
        order=order,
        desc=desc,
        limit=limit,
        offset=offset,
    )


@router.post("/like")
async def like_video(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoLikesDislikes:
    return await video_service.like_video(
        user_id=user.id,
        video_id=video_id,
    )


@router.delete("/like")
async def unlike_video(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoLikesDislikes:
    return await video_service.unlike_video(
        user_id=user.id,
        video_id=video_id,
    )


@router.post("/dislike")
async def dislike_video(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoLikesDislikes:
    return await video_service.dislike_video(
        user_id=user.id,
        video_id=video_id,
    )


@router.delete("/dislike")
async def undislike_video(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoLikesDislikes:
    return await video_service.undislike_video(
        user_id=user.id,
        video_id=video_id,
    )


@router.get("/subscriptions")
async def get_subscriptions(
    order: VideoOrder = VideoOrder.ID,  # type: ignore
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_subscriptions(
        user_id=user.id,
        order=order,
        desc=desc,
        offset=offset,
        limit=limit,
    )


@router.get("/playlist")
async def get_playlist_videos(
    playlist_id: UUID,
    offset: int = 0,
    limit: int = 100,
    user: UserGet | None = Depends(get_current_optional_user),
    video_service: VideoService = Depends(get_video_service),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> list[VideoGet]:
    playlist = await playlist_service.get_playlist_by_id(playlist_id=playlist_id, user=user)

    return await video_service.get_playlist_videos(
        playlist_id=playlist.id,
        limit=limit,
        offset=offset,
    )
