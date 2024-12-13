import uuid
import datetime
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.config import settings
from src.models import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    session_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    @property
    def issued_at(self) -> datetime.datetime:
        return self.expires_at - datetime.timedelta(minutes=settings.admin_settings.admin_sesion_expire_minutes)
