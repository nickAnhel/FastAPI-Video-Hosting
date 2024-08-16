from fastapi import HTTPException, status
from fastapi.requests import Request

from app.videos.exceptions import (
    VideoNotFound,
    VideoTitleAlreadyExists,
    VideoDataWrongFormat,
    PermissionDenied,
    CantUploadVideoToS3,
    CantUploadPreviewToS3,
    CantDeleteVideoFromS3,
    CantDeleteComments,
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


async def permission_denied_handler(request: Request, exc: PermissionDenied) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )


async def cant_upload_video_to_s3_handler(request: Request, exc: CantUploadVideoToS3) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )


async def cant_upload_preview_to_s3_handler(request: Request, exc: CantUploadPreviewToS3) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )


async def cant_delete_video_from_s3_handler(request: Request, exc: CantDeleteVideoFromS3) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )


async def cant_delete_comments_handler(request: Request, exc: CantDeleteComments) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )
