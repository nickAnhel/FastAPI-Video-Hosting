from uuid import UUID
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.playlists.external import get_user_id_by_token
from app.playlists.exceptions import CantGetUserID


def _get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    return credentials.credentials


async def get_current_user_id(
    token: str = Depends(_get_token_from_header),
) -> UUID:
    try:
        user_id = await get_user_id_by_token(token=token)
        return UUID(user_id)
    except CantGetUserID as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


# TODO: Make it good
def _get_optional_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str | None:
    return credentials.credentials if credentials else None


async def get_optional_user_id(
    token: str | None = Depends(_get_optional_token_from_header),
) -> UUID | None:
    if not token:
        return None

    try:
        user_id = await get_user_id_by_token(token=token)
        return UUID(user_id)
    except CantGetUserID as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc
