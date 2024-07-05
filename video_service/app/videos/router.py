from uuid import UUID
from fastapi import APIRouter, Depends

from app.videos.scemas import VideoCreate
from app.videos.service import VideoService
from app.videos.dependencies import get_video_service


video_router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@video_router.post("/")
async def create_video(
    data: VideoCreate,
    video_service: VideoService = Depends(get_video_service),
):
    return await video_service.create_video(data=data)


@video_router.get("/")
async def get_videos(
    order: str = "id",
    offset: int = 0,
    limit: int = 100,
    video_service: VideoService = Depends(get_video_service),
):
    return await video_service.get_videos(
        order=order,
        offset=offset,
        limit=limit,
    )


@video_router.get("/{video_id}")
async def get_video_by_id(
    video_id: UUID,
    video_service: VideoService = Depends(get_video_service),
):
    return await video_service.get_video(id=video_id)


@video_router.delete("/")
async def delete_video(
    video_id: UUID,
    video_service: VideoService = Depends(get_video_service),
):
    await video_service.delete_video(id=video_id)
