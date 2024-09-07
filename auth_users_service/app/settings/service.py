import uuid

from app.settings.repository import SettingsRepository
from app.settings.schemas import SettingsGet, SettingsUpdate


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
        user_id: uuid.UUID,
        data: SettingsUpdate,
    ) -> SettingsGet:
        return await self._repository.update(data, user_id=user_id)
