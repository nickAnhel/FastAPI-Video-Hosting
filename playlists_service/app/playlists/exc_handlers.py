from fastapi import Request, HTTPException, status

from app.playlists.exceptions import (
    PlaylistNotFound,
    PermissionDenied,
    PlaylistTitleAlreadyExists,
    PlaylistDoesNotContainVideo,
)


async def playlist_not_found_handler(request: Request, exc: PlaylistNotFound) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def permission_denied_handler(request: Request, exc: PermissionDenied) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )


async def playlist_title_already_exists_handler(request: Request, exc: PlaylistTitleAlreadyExists) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    )


async def playlist_not_contain_video_handler(request: Request, exc: PlaylistDoesNotContainVideo) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
