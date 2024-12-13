import uuid
import datetime
from fastapi.requests import Request
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select

from src.config import settings
from src.database import async_session_maker
from src.users.models import UserModel
from src.auth.utils import validate_password

from src.admin.repository import SessionRepository


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        form = await request.form()
        username: str = form.get("username")  # type: ignore
        password: str = form.get("password")  # type: ignore

        async with async_session_maker() as session:
            query = select(UserModel).filter_by(username=username)
            res = await session.execute(query)
            user = res.scalar_one_or_none()

        if user and validate_password(password, user.hashed_password) and user.is_admin:
            session_expires_at = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
                minutes=settings.admin_settings.admin_sesion_expire_minutes
            )
            session_model = await SessionRepository.create(
                user_id=user.id,
                expires_at=session_expires_at,
            )

            request.session.update({"session_id": str(session_model.session_id)})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        try:
            session_id: uuid.UUID = uuid.UUID(request.session.get("session_id"))
            await SessionRepository.delete(session_id=session_id)
        except TypeError:
            pass

        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        try:
            session_id: uuid.UUID = uuid.UUID(request.session.get("session_id"))
        except TypeError:
            return False

        session = await SessionRepository.get(session_id=session_id)

        if not session:
            request.session.clear()
            return False

        if session.expires_at < datetime.datetime.now(tz=datetime.UTC):
            await SessionRepository.delete(session_id=session.session_id)
            request.session.clear()
            return False

        return True
