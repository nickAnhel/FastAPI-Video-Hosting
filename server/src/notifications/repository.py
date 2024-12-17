import uuid
from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.notifications.models import NotificationModel


class NotificationsRepository:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session

    async def create_multi(
        self,
        users_ids: list[uuid.UUID],
        channel_id: uuid.UUID,
        video_id: uuid.UUID,
    ) -> None:
        stmt = (
            insert(NotificationModel)
            .values(
                [
                    {
                        "user_id": user_id,
                        "channel_id": channel_id,
                        "video_id": video_id,
                    }
                    for user_id in users_ids
                ]
            )
        )

        await self._async_session.execute(stmt)
        await self._async_session.commit()

    async def get_multi(
        self,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[NotificationModel]:
        query = (
            select(NotificationModel)
            .filter_by(user_id=user_id)
            .order_by(NotificationModel.created_at.desc())
            .limit(limit)
            .offset(offset)
            .options(selectinload(NotificationModel.channel))
            .options(selectinload(NotificationModel.video))
        )

        update_is_read_stmt = (
            update(NotificationModel)
            .filter_by(
                user_id=user_id,
                is_read=False,
            )
            .values(is_read=True)
        )

        res = await self._async_session.execute(query)

        await self._async_session.execute(update_is_read_stmt)
        await self._async_session.commit()

        return list(res.scalars().all())

    async def get_new_notifications_count(
        self,
        user_id: uuid.UUID,
    ) -> int:
        query = (
            select(func.count("*"))
            .select_from(NotificationModel)
            .filter_by(
                user_id=user_id,
                is_read=False,
            )
        )

        res = await self._async_session.execute(query)
        return res.scalar_one()

    async def delete(
        self,
        notification_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> int:
        stmt = (
            delete(NotificationModel)
            .filter_by(
                id=notification_id,
                user_id=user_id,
            )
        )

        res = await self._async_session.execute(stmt)
        await self._async_session.commit()

        return res.rowcount
