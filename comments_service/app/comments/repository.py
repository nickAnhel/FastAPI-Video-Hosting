from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session
