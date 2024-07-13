from uuid import UUID
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.videos.service import VideoService
from app.videos.repository import VideoRepository
from app.videos.external import get_user_id_by_token
from app.videos.exceptions import CantGetUserID


def get_video_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> VideoService:
    video_repository = VideoRepository(async_session)
    return VideoService(video_repository)


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
