from typing import Any
from uuid import UUID
from sqlalchemy import select, update, delete, desc, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

# from src.videos.models import VideoModel

from src.users.models import UserModel, UserSubscription


class UserRepository:
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    async def create(
        self,
        data: dict[str, Any],
    ) -> UserModel:
        user = UserModel(**data)
        self._async_session.add(user)
        return user

    async def get_single(
        self,
        **filters,
    ) -> UserModel:
        query = (
            select(UserModel)
            .filter_by(**filters)
            .options(selectinload(UserModel.subscribed))
            .options(
                selectinload(UserModel.subscribers)
                .options(selectinload(UserModel.settings))
            )
        )
        result = await self._async_session.execute(query)
        return result.scalar_one()

    async def get_multi(
        self,
        user_id: UUID | None = None,
        order: str = "id",
        order_desc: bool = False,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserModel]:
        query = (
            select(UserModel)
            .order_by(desc(order) if order_desc else order)
            .offset(offset)
            .limit(limit)
        )

        if user_id:
            query  = query.options(selectinload(UserModel.subscribers))

        result = await self._async_session.execute(query)
        return list(result.scalars().all())

    async def search(
        self,
        search_query: str,
        user_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserModel]:
        columns = func.coalesce(UserModel.username, '').concat(func.coalesce(UserModel.about, ''))
        columns = columns.self_group()

        query = (
            select(UserModel)
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
        )

        if user_id:
            query  = query.options(selectinload(UserModel.subscribers))

        res = await self._async_session.execute(query)
        return list(res.scalars().all())

    async def update(
        self,
        data: dict[str, Any],
        **filters,
    ) -> UserModel:
        stmt = (
            update(UserModel)
            .filter_by(**filters)
            .values(**data)
            .returning(UserModel)
        )

        result = await self._async_session.execute(stmt)
        await self._async_session.commit()

        return result.scalar_one()

    async def delete(
        self,
        **filters,
    ) -> int:
        user_query = (
            select(UserModel)
            .filter_by(**filters)
            .options(selectinload(UserModel.subscribed))
            # .options(selectinload(UserModel.liked_videos))
            # .options(selectinload(UserModel.disliked_videos))
        )

        res = await self._async_session.execute(user_query)
        user = res.scalar_one()

        # update_liked_stmt = (
        #     update(VideoModel)
        #     .where(VideoModel.id.in_([v.id for v in user.liked_videos]))
        #     .values(likes=VideoModel.likes - 1)
        # )

        # update_disliked_stmt = (
        #     update(VideoModel)
        #     .where(VideoModel.id.in_([v.id for v in user.disliked_videos]))
        #     .values(dislikes=VideoModel.dislikes - 1)
        # )

        update_subs_count_stmt = (
            update(UserModel)
            .where(UserModel.id.in_([u.id for u in user.subscribed]))
            .values(subscribers_count=UserModel.subscribers_count - 1)
        )

        delete_user_stmt = (
            delete(UserModel)
            .filter_by(**filters)
        )

        # await self.async_session.execute(update_liked_stmt)
        # await self.async_session.execute(update_disliked_stmt)
        await self._async_session.execute(update_subs_count_stmt)
        res = await self._async_session.execute(delete_user_stmt)

        await self._async_session.commit()
        return res.rowcount != 0

    async def subscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        user = await self.get_single(id=user_id)
        subscriber = await self.get_single(id=subscriber_id)

        if subscriber not in user.subscribers:
            user.subscribers.append(subscriber)
            user.subscribers_count += 1
            await self._async_session.commit()

    async def unsubscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        user = await self.get_single(id=user_id)
        subscriber = await self.get_single(id=subscriber_id)

        user.subscribers.remove(subscriber)
        user.subscribers_count -= 1
        await self._async_session.commit()

    async def get_subscriptions(
        self,
        user_id: UUID,
    ) -> list[UserModel]:
        subs_query = (
            select(UserSubscription.subscribed_id)
            .filter_by(subscriber_id=user_id)
            .cte()
        )

        query = (
            select(UserModel)
            .join(subs_query, UserModel.id == subs_query.c.subscribed_id)
            .options(selectinload(UserModel.subscribers))
        )

        res = await self._async_session.execute(query)
        return list(res.scalars().all())
