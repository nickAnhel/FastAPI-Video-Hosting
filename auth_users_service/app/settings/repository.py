import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.models import SettingsModel
from app.settings.schemas import SettingsUpdate, SettingsGet


class SettingsRepository:
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    async def create(
        self,
        user_id: uuid.UUID,
    ) -> None:
        settings = SettingsModel(user_id=user_id)
        self._async_session.add(settings)

    async def get(
        self,
        **filters,
    ) -> SettingsGet:
        query = select(SettingsModel).filter_by(**filters)
        res = await self._async_session.execute(query)
        return SettingsGet.model_validate(res.scalar_one())

    async def update(
        self,
        data: SettingsUpdate,
        **filters,
    ) -> SettingsGet:
        stmt = (
            update(SettingsModel)
            .filter_by(**filters)
            .values(**data.model_dump(exclude_none=True))
            .returning(SettingsModel)
        )
        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return SettingsGet.model_validate(res.scalar_one())
