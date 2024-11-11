from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.playlists.schemas import PlaylistCreate, PlaylistGet
from app.playlists.dependencies import get_playlists_service, get_current_user_id, get_optional_user_id
from app.playlists.service import PlaylistService
from app.playlists.enums import PlaylistOrder


playlists_router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
)


@playlists_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_playlist(
    data: PlaylistCreate,
    user_id: UUID = Depends(get_current_user_id),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> PlaylistGet:
    return await playlist_service.create_playlist(user_id=user_id, data=data)


@playlists_router.get("/list")
async def get_playlists(
    order: PlaylistOrder = PlaylistOrder.ID,
    offset: int = 0,
    limit: int = 100,
    owner_id: UUID | None = None,
    user_id: UUID | None = Depends(get_optional_user_id),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> list[PlaylistGet]:
    return await playlist_service.get_playlists(
        order=order,
        offset=offset,
        limit=limit,
        owner_id=owner_id,
        user_id=user_id,
    )


@playlists_router.get("/")
async def get_playlist_by_id(
    playlist_id: UUID,
    user_id: UUID | None = Depends(get_optional_user_id),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> PlaylistGet:
    return await playlist_service.get_playlist_by_id(playlist_id=playlist_id, user_id=user_id)


@playlists_router.delete("/")
async def delete_playlist_by_id(
    playlist_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> dict[str, str]:
    await playlist_service.delete_playlist_by_id(playlist_id=playlist_id, user_id=user_id)
    return {"detail": "Playlist deleted successfully"}


@playlists_router.patch("/add-video")
async def add_video_to_playlist(
    playlist_id: UUID,
    video_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> PlaylistGet:
    return await playlist_service.add_video_to_playlist(
        playlist_id=playlist_id,
        video_id=video_id,
        user_id=user_id,
    )


@playlists_router.patch("/remove-video")
async def remove_video_from_playlist(
    playlist_id: UUID,
    video_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> PlaylistGet:
    return await playlist_service.remove_video_from_playlist(
        playlist_id=playlist_id,
        video_id=video_id,
        user_id=user_id,
    )
