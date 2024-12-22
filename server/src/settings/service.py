import uuid

from src.users.schemas import UserGet

from src.settings.repository import SettingsRepository
from src.settings.schemas import SettingsGet, SettingsUpdate
from src.settings.exceptions import EmailNotVerified, TelegramNotVerified


class SettingsService:
    _repository: SettingsRepository

    def __init__(self, repository: SettingsRepository) -> None:
        self._repository = repository

    async def get(
        self,
        user_id: uuid.UUID,
    ) -> SettingsGet:
        return await self._repository.get(user_id=user_id)

    async def udpate(
        self,
        user: UserGet,
        data: SettingsUpdate,
    ) -> SettingsGet:
        if data.enable_email_notifications and not user.is_verified_email:
            raise EmailNotVerified("Can't turn on email notifications while email not verified")

        if data.enable_telegram_notifications and not user.is_verified_telegram:
            raise TelegramNotVerified("Can't turn on telegram notifications while telegram not verified")

        return await self._repository.update(data, user_id=user.id)
