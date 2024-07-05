from typing import Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.videos.models import VideoModel


class VideoRepository:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session

    async def create(
        self,
        data: dict[str, Any],
    ) -> VideoModel:
        video = VideoModel(**data)

        self._async_session.add(video)
        await self._async_session.commit()
        await self._async_session.refresh(video)

        return video

    async def get_single(
        self,
        **filters,
    ) -> VideoModel | None:
        query = select(VideoModel).filter_by(**filters)
        video = await self._async_session.execute(query)
        return video.scalar_one_or_none()

    async def get_multi(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoModel]:
        query = (
            select(VideoModel)
            .order_by(order)
            .offset(offset)
            .limit(limit)
        )
        videos = await self._async_session.execute(query)
        return list(videos.scalars().all())

    async def delete(
        self,
        **filters,
    ) -> None:
        stmt = (
            delete(VideoModel)
            .filter_by(**filters)
        )
        await self._async_session.execute(stmt)
        await self._async_session.commit()
