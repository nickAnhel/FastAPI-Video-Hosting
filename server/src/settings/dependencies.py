from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.settings.service import SettingsService
from src.settings.repository import SettingsRepository


def get_settings_service(
    session: AsyncSession = Depends(get_async_session),
) -> SettingsService:
    return SettingsService(
        repository=SettingsRepository(session),
    )
