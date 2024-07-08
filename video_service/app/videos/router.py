from uuid import UUID
from sqlalchemy.exc import IntegrityError, DBAPIError
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    Depends,
    Form,
    status,
)
from fastapi.responses import HTMLResponse

from app.videos.scemas import VideoCreate
from app.videos.service import VideoService
from app.videos.dependencies import get_video_service
from app.videos.exceptions import VideoNotFound, CantUploadVideoToS3, CantDeleteVideoFromS3
from app.videos.scemas import VideoGet
from app.videos.utils import get_s3_storage_url
from app.videos.enums  import VideoOrder


video_router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@video_router.post("/")
async def create_video(
    file: UploadFile,
    title: str = Form(...),
    description: str = Form(...),
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    try:
        data = VideoCreate(title=title, description=description)
        return await video_service.create_video(file=file.file, data=data)  # type: ignore

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


@video_router.get("/")
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


@video_router.get("/watch")
async def watch_video(
    video: UUID,
) -> HTMLResponse:
    url = await get_s3_storage_url()
    return HTMLResponse(content=f"<video src='{url}/{video}' controls></video>")


@video_router.get("/{video_id}")
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
async def delete_video(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> dict[str, str]:
    try:
        await video_service.delete_video(id=video)
        return {"detail": "Video deleted successfully"}
    except VideoNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        ) from exc
    except CantDeleteVideoFromS3 as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete video",
        ) from exc


@video_router.patch("/increment-views")
async def increment_video_views(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.increment_views(id=video)


@video_router.patch("/increment-likes")
async def increment_video_likes(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.increment_likes(id=video)


@video_router.patch("/decrement-likes")
async def decrement_video_likes(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.decrement_likes(id=video)


@video_router.patch("/increment-dislikes")
async def increment_video_dislikes(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.increment_dislikes(id=video)


@video_router.patch("/decrement-dislikes")
async def decrement_video_dislikes(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    return await video_service.decrement_dislikes(id=video)
