from uuid import UUID
from sqlalchemy.exc import IntegrityError
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    Depends,
    Form,
    status,
)

from app.videos.scemas import VideoCreate
from app.videos.service import VideoService
from app.videos.dependencies import get_video_service
from app.videos.exceptions import VideoNotFound, CantUploadVideo, CantDeleteVideo
from app.videos.scemas import VideoGet


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
    except CantUploadVideo as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload video",
        ) from exc


@video_router.get("/")
async def get_videos(
    order: str = "id",
    offset: int = 0,
    limit: int = 100,
    video_service: VideoService = Depends(get_video_service),
) -> list[VideoGet]:
    return await video_service.get_videos(
        order=order,
        offset=offset,
        limit=limit,
    )


@video_router.get("/{video_id}")
async def get_video_by_id(
    video_id: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> VideoGet:
    try:
        return await video_service.get_video(id=video_id)
    except VideoNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        ) from exc


@video_router.delete("/")
async def delete_video(
    video: UUID,
    video_service: VideoService = Depends(get_video_service),
) -> None:
    try:
        await video_service.delete_video(id=video)
    except CantDeleteVideo as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete video",
        ) from exc
