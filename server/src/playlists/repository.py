from uuid import UUID
from typing import Any, Self
from sqlalchemy import insert, select, delete, update, func, or_
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
                .options(selectinload(PlaylistModel.videos))
            )

            playlists = await session.execute(query)
            return list(playlists.scalars().all())

    async def search(
        self,
        search_query: str,
        offset: int = 0,
        limit: int = 100,
    ) -> list[PlaylistModel]:
        async with async_session_maker() as session:
            columns = func.coalesce(PlaylistModel.title, '').concat(func.coalesce(PlaylistModel.description, ''))
            columns = columns.self_group()

            query = (
                select(PlaylistModel)
                .where(
                    or_(
                        columns.bool_op("%")(search_query),
                        columns.ilike(f"%{search_query}%"),
                    )
                )
                .order_by(
                    func.similarity(columns, search_query).desc(),
                )
                .offset(offset)
                .limit(limit)
                .options(selectinload(PlaylistModel.videos))
            )

            playlists = await session.execute(query)
            return list(playlists.scalars().all())

    async def get_user_playlists_exclude_video(
        self,
        video_id: UUID,
        user_id: UUID,
    ) -> list[PlaylistModel]:
        async with async_session_maker() as session:
            query = (
                select(PlaylistModel)
                .filter_by(user_id=user_id)
                .options(selectinload(PlaylistModel.videos))
            )

            res = await session.execute(query)
            return list(res.scalars().all())


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
            stmt1 = (
                insert(PlaylistVideoM2M)
                .values((playlist_id, video_id))
            )

            stmt2 = (
                update(PlaylistModel)
                .filter_by(id=playlist_id)
                .values(videos_count=PlaylistModel.videos_count + 1)
            )

            await session.execute(stmt1)
            await session.execute(stmt2)
            await session.commit()

    async def remove_video(
        self,
        video_id: UUID,
        playlist_id: UUID,
    ) -> int:
        async with async_session_maker() as session:
            stmt1 = (
                delete(PlaylistVideoM2M)
                .filter_by(
                    playlist_id=playlist_id,
                    video_id=video_id,
                )
            )

            stmt2 = (
                update(PlaylistModel)
                .filter_by(id=playlist_id)
                .values(videos_count=PlaylistModel.videos_count - 1)
            )

            res = await session.execute(stmt1)
            res = await session.execute(stmt2)
            await session.commit()
            return res.rowcount
