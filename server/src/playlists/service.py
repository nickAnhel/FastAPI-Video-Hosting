from uuid import UUID
from typing import Self
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import PermissionDenied

from src.users.schemas import UserGet

from src.playlists.repository import PlaylistRepository
from src.playlists.schemas import PlaylistCreate, PlaylistGet, PlaylistGetWithFirstVideo
from src.playlists.enums import PlaylistOrder
from src.playlists.models import PlaylistModel
from src.playlists.exceptions import (
    CantRemoveVideoFromPlaylist,
    CantAddVideoToPlaylist,
    PlaylistNotFound,
)


class PlaylistService:
    __instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self._repository = PlaylistRepository()

    async def create_playlist(
        self,
        user_id: UUID,
        data: PlaylistCreate,
    ) -> PlaylistGet:
        playlist_data = data.model_dump()
        playlist_data["user_id"] = user_id

        playlist = await self._repository.create(playlist_data)
        return PlaylistGet.model_validate(playlist)

    async def get_playlist_by_id(
        self,
        playlist_id: UUID,
        user: UserGet | None = None,
    ) -> PlaylistGetWithFirstVideo:
        playlist = await self._check_playlist_exists(playlist_id=playlist_id)

        if playlist.private and not user:
            raise PermissionDenied(f"Playlist with id {playlist.id} is private")

        if playlist.private and user:
            await self._check_user_permissions(playlist=playlist, user_id=user.id)

        return PlaylistGetWithFirstVideo.model_validate(playlist)

    async def get_playlists(
        self,
        order: PlaylistOrder = PlaylistOrder.ID,
        offset: int = 0,
        limit: int = 100,
        owner_id: UUID | None = None,
        user: UserGet | None = None,
    ) -> list[PlaylistGetWithFirstVideo]:
        params = {"order": order, "offset": offset, "limit": limit}

        if owner_id:
            params["user_id"] = owner_id

        playlists = await self._repository.get_multi(**params)
        playlists = [
            playlist for playlist in playlists if not playlist.private or (user and playlist.user_id == user.id)
        ]

        return [PlaylistGetWithFirstVideo.model_validate(playlist) for playlist in playlists]

    async def delete_playlist_by_id(
        self,
        playlist_id: UUID,
        user_id: UUID,
    ) -> None:
        await self._repository.delete(id=playlist_id, user_id=user_id)

    async def delete_playlist_by_title(
        self,
        title: str,
        user_id: UUID,
    ) -> None:
        await self._repository.delete(title=title, user_id=user_id)

    async def add_video_to_playlist(
        self,
        playlist_id: UUID,
        video_id: UUID,
        user_id: UUID,
    ) -> None:
        await self._check_user_permissions_and_playlist_exists(
            playlist_id=playlist_id,
            user_id=user_id,
        )

        try:
            await self._repository.add_video(video_id=video_id, playlist_id=playlist_id)
        except IntegrityError as exc:
            raise CantAddVideoToPlaylist(f"Can't add video with id {video_id} to playlist") from exc

    async def remove_video_from_playlist(
        self,
        playlist_id: UUID,
        video_id: UUID,
        user_id: UUID,
    ) -> None:
        await self._check_user_permissions_and_playlist_exists(
            playlist_id=playlist_id,
            user_id=user_id,
        )

        if not (await self._repository.remove_video(video_id=video_id, playlist_id=playlist_id)) == 1:
            raise CantRemoveVideoFromPlaylist(f"Can't remove video with id {video_id} from playlist")

    async def _check_playlist_exists(
        self,
        playlist_id: UUID,
    ) -> PlaylistModel:
        try:
            return await self._repository.get_single(id=playlist_id)
        except NoResultFound as exc:
            raise PlaylistNotFound(f"Playlist with id {playlist_id} not found") from exc

    async def _check_user_permissions(
        self,
        playlist: PlaylistModel,
        user_id: UUID | None,
    ) -> None:
        if playlist.user_id != user_id:
            raise PermissionDenied(f"User with id {user_id} is not owner of playlist with id {playlist.id}")

    async def _check_user_permissions_and_playlist_exists(
        self,
        playlist_id: UUID,
        user_id: UUID,
    ) -> PlaylistModel:
        playlist = await self._check_playlist_exists(playlist_id=playlist_id)
        await self._check_user_permissions(playlist=playlist, user_id=user_id)
        return playlist
