from typing import Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.models import CommentModel
from app.comments.enums import CommentOrder


class CommentRepository:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session

    async def create(
        self,
        data: dict[str, Any],
    ) -> CommentModel:
        comment = CommentModel(**data)
        self._async_session.add(comment)

        await self._async_session.commit()
        await self._async_session.refresh(comment)

        return comment

    async def get_single(
        self,
        **filters,
    ) -> CommentModel | None:
        query = select(CommentModel).filter_by(**filters)
        res = await self._async_session.execute(query)
        comment = res.scalar_one_or_none()

        return comment

    async def get_multi(
        self,
        order: CommentOrder = CommentOrder.ID,  # type: ignore
        offset: int = 0,
        limit: int = 100,
        **filters,
    ) -> list[CommentModel]:
        query = select(CommentModel).filter_by(**filters).order_by(order).offset(offset).limit(limit)
        res = await self._async_session.execute(query)
        comments = list(res.scalars().all())

        return comments

    async def delete(
        self,
        **filters,
    ) -> int:
        stmt = delete(CommentModel).filter_by(**filters)

        res = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return res.rowcount
