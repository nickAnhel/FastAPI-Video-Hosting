from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.videos.service import VideoService
from src.videos.repository import VideoRepository


def get_video_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> VideoService:
    video_repository = VideoRepository(async_session)
    return VideoService(video_repository)
