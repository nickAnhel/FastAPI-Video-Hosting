from typing import Annotated
from uuid import UUID
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    Query,
    Depends,
    Form,
    status,
)

from src.videos.schemas import VideoLikesDislikes
from src.schemas import Status

from src.auth.dependencies import get_current_user, get_current_optional_user
from src.users.schemas import UserGet

from src.videos.schemas import VideoGet, VideoCreate
from src.videos.service import VideoService
from src.videos.dependencies import get_video_service
from src.videos.enums import VideoOrder


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.post("/")
async def create_video(
    video: UploadFile,
    preview: UploadFile,
    title: str = Form(...),
    description: str = Form(...),
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
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
    return await video_service.create_video(
        video=video.file,  # type: ignore
        preview=preview.file,  # type: ignore
        data=data,
    )


@router.get("/search")
async def search_videos(
    query: Annotated[str, Query(max_length=50)],
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.search_videos(query=query)


@router.get("/list")
async def get_videos(
    order: VideoOrder = VideoOrder.ID,  # type: ignore
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_videos(
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
) -> VideoGet:
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
) -> VideoGet:
    return await video_service.increment_views(video_id=video_id)


@router.get("/history")
async def get_watch_history(
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_watch_history(user_id=user.id)


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


@router.delete("/unlike")
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


@router.delete("/undislike")
async def undislike_video(
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    video_service: VideoService = Depends(get_video_service),
) -> VideoLikesDislikes:
    return await video_service.undislike_video(
        user_id=user.id,
        video_id=video_id,
    )
