from uuid import UUID
from typing import Annotated
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import Depends

from app.playlists.repository import PlaylistRepository
from app.playlists.schemas import PlaylistCreate, PlaylistGet
from app.playlists.enums import PlaylistOrder
from app.playlists.models import PlaylistModel
from app.playlists.exceptions import (
    PermissionDenied,
    PlaylistDoesNotContainVideo,
    PlaylistNotFound,
    PlaylistTitleAlreadyExists,
)


class PlaylistService:
    def __init__(self, repository: Annotated[PlaylistRepository, Depends()]):
        self._repository = repository

    async def create_playlist(
        self,
        user_id: UUID,
        data: PlaylistCreate,
    ) -> PlaylistGet:
        playlist_data = data.model_dump()
        playlist_data["user_id"] = user_id

        try:
            playlist = await self._repository.create(playlist_data)
            return PlaylistGet.model_validate(playlist)
        except IntegrityError as exc:
            raise PlaylistTitleAlreadyExists(f"Playlist with title {data.title!r} already exists") from exc

    async def get_playlist_by_id(
        self,
        playlist_id: UUID,
        user_id: UUID | None = None,
    ) -> PlaylistGet:
        playlist = await self._check_playlist_exists(playlist_id=playlist_id)

        if playlist.private:
            await self._check_user_permissions(playlist=playlist, user_id=user_id)

        return PlaylistGet.model_validate(playlist)

    async def get_playlists(
        self,
        order: PlaylistOrder = PlaylistOrder.ID,
        offset: int = 0,
        limit: int = 100,
        owner_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> list[PlaylistGet]:
        params = {"order": order, "offset": offset, "limit": limit}

        if owner_id:
            params["user_id"] = owner_id

        playlists = await self._repository.get_multi(**params)
        playlists = [playlist for playlist in playlists if not playlist.private or playlist.user_id == user_id]

        return [PlaylistGet.model_validate(playlist) for playlist in playlists]

    async def delete_playlist_by_id(
        self,
        playlist_id: UUID,
        user_id: UUID,
    ) -> None:
        await self._check_user_permissions_and_playlist_exists(
            playlist_id=playlist_id,
            user_id=user_id,
        )
        await self._repository.delete(id=playlist_id, user_id=user_id)

    async def add_video_to_playlist(
        self,
        playlist_id: UUID,
        video_id: UUID,
        user_id: UUID,
    ) -> PlaylistGet:
        await self._check_user_permissions_and_playlist_exists(
            playlist_id=playlist_id,
            user_id=user_id,
        )

        playlist = await self._repository.add_video(video_id=video_id, id=playlist_id)
        return PlaylistGet.model_validate(playlist)

    async def remove_video_from_playlist(
        self,
        playlist_id: UUID,
        video_id: UUID,
        user_id: UUID,
    ) -> PlaylistGet:
        await self._check_user_permissions_and_playlist_exists(
            playlist_id=playlist_id,
            user_id=user_id,
        )
        try:
            playlist = await self._repository.remove_video(video_id=video_id, id=playlist_id)
            return PlaylistGet.model_validate(playlist)
        except ValueError as exc:
            raise PlaylistDoesNotContainVideo(
                f"Playlist with id {playlist_id} does not contain video with id {video_id}"
            ) from exc

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
