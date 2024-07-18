from uuid import UUID
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.comments.service import CommentService
from app.comments.repository import CommentRepository
from app.comments.external import get_user_id_by_token
from app.comments.exceptions import CantGetUserID


def get_comment_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> CommentService:
    comment_repository = CommentRepository(async_session)
    return CommentService(comment_repository)


def _get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    return credentials.credentials


async def get_current_user_id(
    token: str = Depends(_get_token_from_header),
) -> UUID:
    http_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization token",
    )
    try:
        user_id = await get_user_id_by_token(token=token)
        return UUID(user_id)
    except ValueError as exc:
        raise http_exception from exc
    except CantGetUserID as exc:
        raise http_exception from exc
