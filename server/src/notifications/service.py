import uuid
from pathlib import Path
from jinja2 import Template

from src.schemas import Email, Telegram
from src.config import settings

from src.users.schemas import UserGet, UserGetWithSubscriptions
from src.videos.schemas import VideoGet

from src.notifications.repository import NotificationsRepository
from src.notifications.schemas import NotificationGet
from src.notifications.exceptions import NotificationNotFound
from src.notifications.utils import send_notification


BASE_DIR = Path(__file__).parent.parent.parent


class NotificationsService:
    def __init__(self, repository: NotificationsRepository):
        self._repository = repository

    async def send_notification_to_user_subs(
        self,
        user: UserGetWithSubscriptions,
        video: VideoGet,
    ) -> None:
        await self._repository.create_multi(
            users_ids=[u.id for u in user.subscribers],
            channel_id=user.id,
            video_id=video.id,
        )

        for u in user.subscribers:
            if u.settings.enable_email_notifications:
                with open(BASE_DIR / "templates" / "email_notification.html", "r", encoding="utf-8") as file:
                    template = Template(file.read())

                email_body = template.render(
                    channel_link=f"{settings.url_settings.frontend_host}/channels/{user.id}",
                    channel=user.username,
                    video_link=f"{settings.url_settings.frontend_host}/videos/{video.id}",
                    video_title=video.title,
                )

                message = Email(
                    email=u.email,
                    subject="New video published",
                    content=email_body,
                )

                await send_notification(message)

            if u.settings.enable_telegram_notifications:
                with open(BASE_DIR / "templates" / "telegram_notification.html", "r", encoding="utf-8") as file:
                    template = Template(file.read())

                telegram_body = template.render(
                    channel_link=f"{settings.url_settings.frontend_host}/channels/{user.id}",
                    channel=user.username,
                    video_link=f"{settings.url_settings.frontend_host}/videos/{video.id}",
                    video_title=video.title,
                )

                message = Telegram(
                    chat_id=u.telegram_chat_id,
                    content=telegram_body,
                    preview_url=f"{settings.storage_settings.storage_url}/{settings.file_prefixes.preview}{video.id}.jpg",
                )

                await send_notification(message)

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
