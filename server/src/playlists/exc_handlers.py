from fastapi import Request, HTTPException, status

from src.playlists.exceptions import (
    PlaylistNotFound,
    CantAddVideoToPlaylist,
    CantRemoveVideoFromPlaylist,
)


async def playlist_not_found_handler(request: Request, exc: PlaylistNotFound) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def cant_remove_video_handler(request: Request, exc: CantRemoveVideoFromPlaylist) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


async def cant_add_video_handler(request: Request, exc: CantAddVideoToPlaylist) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
