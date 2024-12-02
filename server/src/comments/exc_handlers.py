from fastapi import HTTPException, status
from fastapi.requests import Request

from src.comments.exceptions import (
    CommentNotFound,
    CommentContentWrongFormat,
)


async def comment_not_found_handler(request: Request, exc: CommentNotFound):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def comment_content_wrong_format_handler(request: Request, exc: CommentContentWrongFormat):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
