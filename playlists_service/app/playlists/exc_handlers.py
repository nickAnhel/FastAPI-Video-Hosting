from fastapi import Request, HTTPException, status

from app.playlists.exceptions import PlaylistNotFound, PermissionDenied


async def playlist_not_found_handler(request: Request, exc: PlaylistNotFound):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def permission_denied_handler(request: Request, exc: PermissionDenied):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )
