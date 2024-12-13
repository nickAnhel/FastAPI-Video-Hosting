import uuid
import datetime
from sqlalchemy import insert, select, delete

from src.database import async_session_maker
from src.admin.models import SessionModel


class SessionRepository:
    @staticmethod
    async def create(
        user_id: uuid.UUID,
        expires_at: datetime.datetime,
    ) -> SessionModel:
        async with async_session_maker() as session:
            stmt = (
                insert(SessionModel)
                .values(
                    user_id=user_id,
                    expires_at=expires_at,
                )
                .returning(SessionModel)
            )

            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @staticmethod
    async def get(
        session_id: uuid.UUID,
    ) -> SessionModel | None:
        async with async_session_maker() as session:
            query = (
                select(SessionModel)
                .filter_by(session_id=session_id)
            )

            res = await session.execute(query)
            return res.scalar_one_or_none()

    @staticmethod
    async def delete(
        session_id: uuid.UUID,
    ) -> None:
        async with async_session_maker() as session:
            stmt = (
                delete(SessionModel)
                .filter_by(session_id=session_id)
            )

            await session.execute(stmt)
            await session.commit()
