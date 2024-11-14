from typing import Any
from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
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
        return user

    async def get_single(
        self,
        **filters,
    ) -> UserModel:
        query = (
            select(UserModel)
            .filter_by(**filters)
            .options(selectinload(UserModel.subscribers))
            .options(selectinload(UserModel.subscribed))
        )
        result = await self.async_session.execute(query)
        return result.scalar_one()

    async def get_multiple(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserModel]:
        query = select(UserModel).order_by(order).offset(offset).limit(limit)

        result = await self.async_session.execute(query)
        return list(result.scalars().all())

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

        result = await self.async_session.execute(stmt)
        await self.async_session.commit()

        return result.scalar_one()

    async def delete(
        self,
        **filters,
    ) -> int:
        stmt = delete(UserModel).filter_by(**filters)
        res = await self.async_session.execute(stmt)
        await self.async_session.commit()
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
            await self.async_session.commit()

    async def unsubscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        user = await self.get_single(id=user_id)
        subscriber = await self.get_single(id=subscriber_id)

        user.subscribers.remove(subscriber)
        user.subscribers_count -= 1
        await self.async_session.commit()
