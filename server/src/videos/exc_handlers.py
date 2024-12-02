from fastapi import HTTPException, status
from fastapi.requests import Request

from src.videos.exceptions import (
    VideoNotFound,
    VideoTitleAlreadyExists,
    VideoDataWrongFormat,
)


async def video_not_found_handler(request: Request, exc: VideoNotFound) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def video_title_already_exists_handler(request: Request, exc: VideoTitleAlreadyExists) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    )


async def video_data_wrong_format_handler(request: Request, exc: VideoDataWrongFormat) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
