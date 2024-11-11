from uuid import UUID
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.playlists.external import get_user_id_by_token
from app.playlists.exceptions import CantGetUserID
from app.playlists.service import PlaylistService


def get_playlists_service() -> PlaylistService:
    return PlaylistService()


def _get_optional_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str | None:
    return credentials.credentials if credentials else None


def get_user_id_closure(
    optional: bool = False,
):
    async def get_user_id_wrapper(
        token: str | None = Depends(_get_optional_token_from_header),
    ) -> UUID | None:
        if optional and not token:
            return None

        try:
            user_id = await get_user_id_by_token(token=token)
            return UUID(user_id)
        except CantGetUserID as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token",
            ) from exc

    return get_user_id_wrapper


get_current_user_id = get_user_id_closure()
get_optional_user_id = get_user_id_closure(optional=True)
