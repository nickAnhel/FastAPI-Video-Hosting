from uuid import UUID
from typing import Any, Self
from sqlalchemy import select, delete

from app.playlists.models import PlaylistModel
from app.database import async_session_maker


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
            playlist = PlaylistModel(**data)

            session.add(playlist)
            await session.commit()
            await session.refresh(playlist)

            return playlist

    async def get_single(
        self,
        **filters,
    ) -> PlaylistModel:
        async with async_session_maker() as session:
            query = select(PlaylistModel).filter_by(**filters)
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
            query = select(PlaylistModel).filter_by(**filters).order_by(order).offset(offset).limit(limit)

            playlists = await session.execute(query)
            return list(playlists.scalars().all())

    async def delete(
        self,
        **filters,
    ) -> int:
        async with async_session_maker() as session:
            stmt = delete(PlaylistModel).filter_by(**filters)
            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount

    async def add_video(
        self,
        video_id: UUID,
        **filters,
    ) -> PlaylistModel:
        async with async_session_maker() as session:
            playlist = await self.get_single(**filters)

            if video_id not in playlist.video_ids:
                playlist.video_ids = list(playlist.video_ids)
                playlist.video_ids.append(video_id)
                await session.commit()
                await session.refresh(playlist)

            return playlist

    async def remove_video(
        self,
        video_id: UUID,
        **filters,
    ) -> PlaylistModel:
        async with async_session_maker() as session:
            playlist = await self.get_single(**filters)

            playlist.video_ids = list(playlist.video_ids)
            playlist.video_ids.remove(video_id)
            await session.commit()
            await session.refresh(playlist)

            return playlist
