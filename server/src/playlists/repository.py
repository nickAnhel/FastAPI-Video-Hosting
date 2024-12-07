from uuid import UUID
from typing import Any, Self
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import selectinload

from src.database import async_session_maker

from src.playlists.models import PlaylistModel, PlaylistVideoM2M


class PlaylistRepository:
    __instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    async def create(
        self,
        data: dict[str, Any],
    ) -> PlaylistModel:
        async with async_session_maker() as session:
            stmt = (
                insert(PlaylistModel)
                .values(data)
                .returning(PlaylistModel)
                .options(selectinload(PlaylistModel.videos))
            )

            res = await session.execute(stmt)
            playlist = res.scalar_one()
            await session.commit()

            return playlist


    async def get_single(
        self,
        **filters,
    ) -> PlaylistModel:
        async with async_session_maker() as session:
            query = (
                select(PlaylistModel)
                .filter_by(**filters)
                .options(selectinload(PlaylistModel.videos))
            )
            playlist = await session.execute(query)
            return playlist.scalar_one()

    async def get_multi(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
        **filters,
    ) -> list[PlaylistModel]:
        async with async_session_maker() as session:
            query = (
                select(PlaylistModel)
                .filter_by(**filters)
                .order_by(order)
                .offset(offset)
                .limit(limit)
            )

            playlists = await session.execute(query)
            return list(playlists.scalars().all())

    async def delete(
        self,
        **filters,
    ) -> int:
        async with async_session_maker() as session:
            stmt = (
                delete(PlaylistModel)
                .filter_by(**filters)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount

    async def add_video(
        self,
        video_id: UUID,
        playlist_id: UUID,
    ) -> None:
        async with async_session_maker() as session:
            stmt = (
                insert(PlaylistVideoM2M)
                .values((playlist_id, video_id))
            )

            await session.execute(stmt)
            await session.commit()

    async def remove_video(
        self,
        video_id: UUID,
        playlist_id: UUID,
    ) -> int:
        async with async_session_maker() as session:
            stmt = (
                delete(PlaylistVideoM2M)
                .filter_by(
                    playlist_id=playlist_id,
                    video_id=video_id,
                )
            )

            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount
