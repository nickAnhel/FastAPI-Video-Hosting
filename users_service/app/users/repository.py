from typing import Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import UserModel


class UserRepository:
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def create(
        self,
        data: dict[str, Any],
    ) -> UserModel:
        user = UserModel(**data)
        self.async_session.add(user)
        await self.async_session.commit()
        await self.async_session.refresh(user)
        return user

    async def get_single(
        self,
        **filters,
    ) -> UserModel | None:
        query = select(UserModel).filter_by(**filters)
        result = await self.async_session.execute(query)
        return result.scalar_one_or_none()

    async def get_multiple(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserModel]:
        query = select(UserModel).order_by(order).offset(offset).limit(limit)

        result = await self.async_session.execute(query)
        return list(result.scalars().all())

    async def delete(
        self,
        **filters,
    ) -> int:
        stmt = delete(UserModel).filter_by(**filters)

        res = await self.async_session.execute(stmt)
        await self.async_session.commit()
        return res.rowcount != 0
