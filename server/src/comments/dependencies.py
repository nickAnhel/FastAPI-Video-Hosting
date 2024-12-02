from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.comments.service import CommentService
from src.comments.repository import CommentRepository


def get_comment_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> CommentService:
    comment_repository = CommentRepository(async_session)
    return CommentService(comment_repository)
