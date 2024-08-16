from fastapi import HTTPException, status
from fastapi.requests import Request

from app.comments.exceptions import (
    CommentNotFound,
    PermissionDenied,
    CommentContentWrongFormat,
)


async def comment_not_found_handler(request: Request, exc: CommentNotFound):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def permission_denied_handler(request: Request, exc: PermissionDenied):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )


async def comment_content_wrong_format_handler(request: Request, exc: CommentContentWrongFormat):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
