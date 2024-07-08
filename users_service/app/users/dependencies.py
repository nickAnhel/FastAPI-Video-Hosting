from uuid import UUID
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users.repository import UserRepository
from app.users.service import UserService
from app.users.external import get_user_id_from_auth_token
from app.users.exceptions import InvalidAuthToken, UserNotFound


http_bearer = HTTPBearer()


async def get_user_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> UserService:
    repository = UserRepository(async_session)
    return UserService(repository=repository)


async def _get_auth_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return credentials.credentials


async def get_current_user_id(
    access_token: str = Depends(_get_auth_token),
):
    try:
        return await get_user_id_from_auth_token(access_token)
    except InvalidAuthToken as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.get_user(id=user_id)
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc
