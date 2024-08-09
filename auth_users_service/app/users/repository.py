from typing import Any
from uuid import UUID
from sqlalchemy import select, delete
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
        await self.async_session.commit()
        await self.async_session.refresh(user)
        return user

    async def get_single(
        self,
        **filters,
    ) -> UserModel | None:
        query = (
            select(UserModel)
            .filter_by(**filters)
            .options(selectinload(UserModel.subscribers))
            .options(selectinload(UserModel.subscribed))
        )
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

    async def subscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        # query = (
        #     select(UserModel)
        #     .where(or_(UserModel.id == user_id, UserModel.id == subscriber_id))  # type: ignore
        #     .options(selectinload(UserModel.subscribers))
        # )
        # users = await self.async_session.execute(query)
        # subscriber, user  = users.scalars().all()

        user = await self.get_single(id=user_id)
        subscriber = await self.get_single(id=subscriber_id)

        user.subscribers.append(subscriber)  # type: ignore
        await self.async_session.commit()

    async def unsubscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        user = await self.get_single(id=user_id)
        subscriber = await self.get_single(id=subscriber_id)

        user.subscribers.remove(subscriber)  # type: ignore
        await self.async_session.commit()
