import uuid

from src.users.schemas import UserGet, UserGetWithSubscriptions

from src.notifications.repository import NotificationsRepository
from src.notifications.schemas import NotificationGet
from src.notifications.exceptions import NotificationNotFound


class NotificationsService:
    def __init__(self, repository: NotificationsRepository):
        self._repository = repository

    async def send_notification_to_user_subs(
        self,
        user: UserGetWithSubscriptions,
        video_id: uuid.UUID,
    ) -> None:
        await self._repository.create_multi(
            users_ids=[u.id for u in user.subscribers],
            channel_id=user.id,
            video_id=video_id,
        )

    async def get_notifications(
        self,
        user: UserGet,
        offset: int,
        limit: int,
    ) -> list[NotificationGet]:
        notifications = await self._repository.get_multi(
            user_id=user.id,
            offset=offset,
            limit=limit,
        )

        return [NotificationGet.model_validate(n) for n in notifications]

    async def get_new_notifications_count(
        self,
        user: UserGet,
    ) -> int:
        return await self._repository.get_new_notifications_count(user_id=user.id)

    async def delete_notification(
        self,
        notification_id: uuid.UUID,
        user: UserGet,
    ) -> None:
        total_deleted = await self._repository.delete(
            notification_id=notification_id,
            user_id=user.id,
        )

        if total_deleted != 1:
            raise NotificationNotFound("Failed to delete notification")
