import uuid
import datetime
from typing import Any, Literal
from sqlalchemy import insert, select, delete, update, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserSubscription
from src.playlists.models import PlaylistVideoM2M

from src.videos.models import (
    VideoModel,
    LikesModel,
    DislikesModel,
    WatchHistoryModel,
)


class VideoRepository:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session

    async def create(
        self,
        data: dict[str, Any],
    ) -> VideoModel:
        stmt = (
            insert(VideoModel)
            .values(data)
            .returning(VideoModel)
            .options(selectinload(VideoModel.user))
        )

        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.scalar_one()

    async def search(
        self,
        search_query: str,
    ) -> list[VideoModel]:
        query = (
            select(VideoModel)
            .filter(VideoModel.title.contains(search_query))
        )
        res = await self._async_session.execute(query)
        videos = list(res.scalars().all())
        return videos

    async def get_single(
        self,
        **filters,
    ) -> VideoModel | None:
        query = (
            select(VideoModel)
            .filter_by(**filters)
            .options(selectinload(VideoModel.user))
        )
        video = await self._async_session.execute(query)
        return video.scalar_one_or_none()

    async def get_multi(
        self,
        order: str = "id",
        order_desc: bool = True,
        offset: int = 0,
        limit: int = 100,
        **filters,
    ) -> list[VideoModel]:
        query = (
            select(VideoModel)
            .filter_by(**filters)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
            .options(selectinload(VideoModel.user))
        )
        videos = await self._async_session.execute(query)
        return list(videos.scalars().all())

    async def delete(
        self,
        **filters,
    ) -> int:
        stmt = delete(VideoModel).filter_by(**filters)
        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.rowcount

    async def get_watch_history(
        self,
        user_id: uuid.UUID,
        order: str = "id",
        order_desc: bool = True,
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoModel]:
        history_query = (
            select(WatchHistoryModel.video_id)
            .filter_by(user_id=user_id)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
            .cte()
        )

        query = (
            select(VideoModel)
            .join(history_query, VideoModel.id == history_query.c.video_id)
            .options(selectinload(VideoModel.user))
        )

        res = await self._async_session.execute(query)
        return list(res.scalars().all())

    async def add_to_watch_history(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> None:
        stmt = (
            pg_insert(WatchHistoryModel)
            .values((user_id, video_id))
            .on_conflict_do_update(
                index_elements=["video_id", "user_id"],
                set_=dict(watched_at=datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None))
            )
        )

        await self._async_session.execute(stmt)
        await self._async_session.commit()


    async def remove_from_watch_history(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> int:
        stmt = (
            delete(WatchHistoryModel)
            .filter_by(
                user_id=user_id,
                video_id=video_id,
            )
        )

        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.rowcount

    async def clear_history(
        self,
        user_id: uuid.UUID,
    ) -> None:
        stmt = (
            delete(WatchHistoryModel)
            .filter_by(user_id=user_id)
        )
        await self._async_session.execute(stmt)
        await self._async_session.commit()

    async def update_watched_at(
        self,
        video_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> None:
        stmt = (
            update(WatchHistoryModel)
            .filter_by(video_id=video_id, user_id=user_id)
            .values(watched_at=datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None))
        )
        await self._async_session.execute(stmt)
        await self._async_session.commit()

    async def get_liked(
        self,
        user_id: uuid.UUID,
        order: str = "id",
        order_desc: bool = True,
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoModel]:
        liked_query = (
            select(LikesModel.video_id)
            .filter_by(user_id=user_id)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
            .cte()
        )

        query = (
            select(VideoModel)
            .join(liked_query, VideoModel.id == liked_query.c.video_id)
            .options(selectinload(VideoModel.user))
        )

        res = await self._async_session.execute(query)
        return list(res.scalars().all())


    async def _update_integer_column(
        self,
        shift: int,
        column: Literal["views", "likes", "dislikes"],
        **filters,
    ) -> VideoModel | None:
        match column:
            case "views":
                col = VideoModel.views
            case "likes":
                col = VideoModel.likes
            case "dislikes":
                col = VideoModel.dislikes

        stmt = (
            update(VideoModel)
            .filter_by(**filters)
            .values({column: col + shift})
            .returning(VideoModel)
            .options(selectinload(VideoModel.user))
        )
        video = await self._async_session.execute(stmt)
        await self._async_session.commit()

        return video.scalar_one_or_none()

    async def increment(
        self,
        column: Literal["views", "likes", "dislikes"],
        **filters,
    ) -> VideoModel | None:
        return await self._update_integer_column(1, column, **filters)

    async def decrement(
        self,
        column: Literal["views", "likes", "dislikes"],
        **filters,
    ) -> VideoModel | None:
        return await self._update_integer_column(-1, column, **filters)

    async def get_stats(
        self,
        **filters,
    ) -> tuple[int, int, int]:
        query = (
            select(VideoModel.likes, VideoModel.dislikes, VideoModel.views)
            .filter_by(**filters)
        )

        res = await self._async_session.execute(query)
        likes, dislikes, views = res.first()  # type: ignore
        return likes, dislikes, views

    async def like(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> None:
        stmt = (
            insert(LikesModel)
            .values((user_id, video_id))
        )

        await self._async_session.execute(stmt)
        await self._async_session.commit()

    async def unlike(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> int:
        stmt = (
            delete(LikesModel)
            .filter_by(
                user_id=user_id,
                video_id=video_id,
            )
        )

        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.rowcount

    async def dislike(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> None:
        stmt = (
            insert(DislikesModel)
            .values((user_id, video_id))
        )

        await self._async_session.execute(stmt)
        await self._async_session.commit()

    async def undislike(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> int:
        stmt = (
            delete(DislikesModel)
            .filter_by(
                user_id=user_id,
                video_id=video_id,
            )
        )

        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.rowcount

    async def is_liked(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> bool:
        query = (
            select(LikesModel)
            .filter_by(
                user_id=user_id,
                video_id=video_id,
            )
        )

        res = await self._async_session.execute(query)
        return len(res.scalars().all()) == 1

    async def is_disliked(
        self,
        user_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> bool:
        query = (
            select(DislikesModel)
            .filter_by(
                user_id=user_id,
                video_id=video_id,
            )
        )

        res = await self._async_session.execute(query)
        return len(res.scalars().all()) == 1

    async def get_subscriptions(
        self,
        user_id: uuid.UUID,
        order: str = "id",
        order_desc: bool = True,
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoModel]:
        subs_query = (
            select(UserSubscription.subscribed_id)
            .filter_by(subscriber_id=user_id)
            .cte()
        )

        query = (
            select(VideoModel)
            .join(subs_query, VideoModel.user_id == subs_query.c.subscribed_id)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
            .options(selectinload(VideoModel.user))
        )

        res = await self._async_session.execute(query)
        return list(res.scalars().all())

    async def get_playlist_videos(
        self,
        playlist_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoModel]:
        playlist_query = (
            select(PlaylistVideoM2M.video_id)
            .filter_by(playlist_id=playlist_id)
            .offset(offset)
            .limit(limit)
            .cte()
        )

        query = (
            select(VideoModel)
            .join(playlist_query, VideoModel.id == playlist_query.c.video_id)
            .options(selectinload(VideoModel.user))
        )

        res = await self._async_session.execute(query)
        return list(res.scalars().all())
