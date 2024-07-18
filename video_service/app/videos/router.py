from uuid import UUID
from sqlalchemy.exc import IntegrityError, DBAPIError
from fastapi.responses import HTMLResponse
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    UploadFile,
    Depends,
    Form,
    status,
)

from app.config import settings
from app.videos.schemas import VideoCreate
from app.videos.service import VideoService
from app.videos.dependencies import get_video_service, get_current_user_id
from app.videos.schemas import VideoGet
from app.videos.external import get_s3_storage_url
from app.videos.enums import VideoOrder
from app.videos.exceptions import (
    PermissionDenied,
    VideoNotFound,
    CantUploadVideoToS3,
    CantUploadPreviewToS3,
    CantDeleteVideoFromS3,
)


video_router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@video_router.post("/")
async def create_video(
    video: UploadFile,
    preview: UploadFile,
    title: str = Form(...),
    description: str = Form(...),
    user_id: UUID = Depends(get_current_user_id),
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

    try:
        data = VideoCreate(title=title, description=description, user_id=user_id)
        return await video_service.create_video(
            video=video.file,  # type: ignore
            preview=preview.file,  # type: ignore
            data=data,
        )

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Video with this title already exists",
        ) from exc

    except DBAPIError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title or description is too long",
        ) from exc

    except CantUploadVideoToS3 as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload video",
        ) from exc

    except CantUploadPreviewToS3 as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload preview",
        ) from exc


@video_router.get("/search")
async def search_videos(
    query: str,
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.search_videos(query=query)


@video_router.get("/list")
async def get_videos(
    order: VideoOrder = VideoOrder.ID,  # type: ignore
    offset: int = 0,
    limit: int = 100,
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_videos(
        order=order,
        offset=offset,
        limit=limit,
    )


@video_router.get("/")
async def get_video_by_id(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    try:
        return await video_service.get_video(id=video)
    except VideoNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        ) from exc


@video_router.delete("/")
async def delete_video_by_id(
    request: Request,
    video: UUID,
    user_id: UUID = Depends(get_current_user_id),
    video_service: VideoService = Depends(get_video_service),
) -> dict[str, str]:
    try:
        await video_service.delete_video(
            token=request.headers.get("Authorization").replace("Bearer ", ""),  # type: ignore
            id=video,
            user_id=user_id,
        )
        return {"detail": "Video deleted successfully"}

    except VideoNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        ) from exc

    except PermissionDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete this video",
        ) from exc

    except CantDeleteVideoFromS3 as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete video",
        ) from exc


@video_router.delete("/list")
async def delete_videos(
    request: Request,
    user_id: UUID = Depends(get_current_user_id),
    video_service: VideoService = Depends(get_video_service),
) -> dict[str, str]:
    try:
        deleted_videos_count = await video_service.delete_videos(
            token=request.headers.get("Authorization").replace("Bearer ", ""),  # type: ignore
            user_id=user_id,
        )
        return {"detail": f"Successfully deleted {deleted_videos_count} videos"}

    except CantDeleteVideoFromS3 as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete video",
        ) from exc


@video_router.patch("/increment/views")
async def increment_video_views(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.increment_views(id=video)


@video_router.patch("/increment/likes")
async def increment_video_likes(
    video: UUID,
    user_id: UUID = Depends(get_current_user_id),
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.increment_likes(id=video)


@video_router.patch("/decrement/likes")
async def decrement_video_likes(
    video: UUID,
    user_id: UUID = Depends(get_current_user_id),
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.decrement_likes(id=video)


@video_router.patch("/increment/dislikes")
async def increment_video_dislikes(
    video: UUID,
    user_id: UUID = Depends(get_current_user_id),
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.increment_dislikes(id=video)


@video_router.patch("/decrement/dislikes")
async def decrement_video_dislikes(
    video: UUID,
    user_id: UUID = Depends(get_current_user_id),
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.decrement_dislikes(id=video)


# Test routes
@video_router.get("/test/watch")
async def watch_video(
    video: UUID,
) -> HTMLResponse:
    storage_url = await get_s3_storage_url()
    video_url = f"{storage_url}/{settings.file_prefixes.video_file + str(video)}"
    preview_url = f"{storage_url}/{settings.file_prefixes.preview_file + str(video)}"
    return HTMLResponse(
        content=f"<video src='{video_url}' poster='{preview_url}' width='960' height='540' controls></video>"
    )


@video_router.get("/test/search")
async def test_search_videos(
    query: str,
    video_service: VideoService = Depends(get_video_service),
) -> HTMLResponse:
    storage_url = await get_s3_storage_url()
    videos = await video_service.search_videos(query=query)
    content = f"""
<h1>{query}</h1>
{[
    f"<video src='{storage_url}/{settings.file_prefixes.video_file + str(video.id)}' controls poster='{storage_url}/{settings.file_prefixes.preview_file + str(video.id)}' width='960' height='540'></video>"
    for video in videos
]}
"""
    return HTMLResponse(content=content)
