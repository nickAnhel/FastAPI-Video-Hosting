from uuid import UUID
from fastapi import APIRouter, Depends, status

from src.schemas import Status
from src.auth.dependencies import get_current_user, get_current_optional_user
from src.users.schemas import UserGet

from src.playlists.schemas import PlaylistCreate, PlaylistGet, PlaylistGetWithVideos
from src.playlists.dependencies import get_playlists_service
from src.playlists.service import PlaylistService
from src.playlists.enums import PlaylistOrder


router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_playlist(
    data: PlaylistCreate,
    user: UserGet = Depends(get_current_user),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> PlaylistGet:
    return await playlist_service.create_playlist(user_id=user.id, data=data)


@router.get("/list")
async def get_playlists(
    order: PlaylistOrder = PlaylistOrder.ID,
    offset: int = 0,
    limit: int = 100,
    owner_id: UUID | None = None,
    user: UserGet = Depends(get_current_optional_user),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> list[PlaylistGet]:
    return await playlist_service.get_playlists(
        order=order,
        offset=offset,
        limit=limit,
        owner_id=owner_id,
        user=user,
    )


@router.get("/")
async def get_playlist_by_id(
    playlist_id: UUID,
    user: UserGet = Depends(get_current_optional_user),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> PlaylistGetWithVideos:
    return await playlist_service.get_playlist_by_id(playlist_id=playlist_id, user=user)


@router.delete("/")
async def delete_playlist_by_id(
    playlist_id: UUID,
    user: UserGet = Depends(get_current_user),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> Status:
    await playlist_service.delete_playlist_by_id(playlist_id=playlist_id, user_id=user.id)
    return Status(detail="Video removed successfully")


@router.post("/add-video")
async def add_video_to_playlist(
    playlist_id: UUID,
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> Status:
    await playlist_service.add_video_to_playlist(
        playlist_id=playlist_id,
        video_id=video_id,
        user_id=user.id,
    )

    return Status(detail="Video added successfully")


@router.delete("/remove-video")
async def remove_video_from_playlist(
    playlist_id: UUID,
    video_id: UUID,
    user: UserGet = Depends(get_current_user),
    playlist_service: PlaylistService = Depends(get_playlists_service),
) -> Status:
    await playlist_service.remove_video_from_playlist(
        playlist_id=playlist_id,
        video_id=video_id,
        user_id=user.id,
    )

    return Status(detail="Video removed successfully")
