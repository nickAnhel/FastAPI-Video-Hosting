from uuid import UUID
from typing import Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.playlists.models import PlaylistModel


class PlaylistRepository:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session

    async def create(
        self,
        data: dict[str, Any],
    ) -> PlaylistModel:
        playlist = PlaylistModel(**data)

        self._async_session.add(playlist)
        await self._async_session.commit()
        await self._async_session.refresh(playlist)

        return playlist

    async def get_single(
        self,
        **filters,
    ) -> PlaylistModel:
        query = select(PlaylistModel).filter_by(**filters)
        playlist = await self._async_session.execute(query)
        return playlist.scalar_one()

    async def get_multi(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
        **filters,
    ) -> list[PlaylistModel]:
        query = (
            select(PlaylistModel)
            .filter_by(**filters)
            .order_by(order)
            .offset(offset)
            .limit(limit)
        )

        playlists = await self._async_session.execute(query)
        return list(playlists.scalars().all())

    async def delete(
        self,
        **filters,
    ) -> int:
        stmt = delete(PlaylistModel).filter_by(**filters)
        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.rowcount

    # async def add_video(
    #     self,
    #     video_id: UUID,
    #     **filters,
    # ) -> PlaylistModel:
    #     playlist = await self.get_single(**filters)

    #     if video_id not in playlist.video_ids:
    #         playlist.video_ids.append(video_id)
    #         await self._async_session.commit()
    #         await self._async_session.refresh(playlist)

    #     return playlist

    # async def remove_video(
    #     self,
    #     video_id: UUID,
    #     **filters,
    # ) -> PlaylistModel:
    #     playlist = await self.get_single(**filters)

    #     playlist.video_ids.remove(video_id)
    #     await self._async_session.commit()
    #     await self._async_session.refresh(playlist)

    #     return playlist
