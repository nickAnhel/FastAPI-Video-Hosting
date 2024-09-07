import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class SettingsModel(Base):
    __tablename__ = "settings"
    __table_args__ = (UniqueConstraint("user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="settings")  # type: ignore

    enable_telegram_notifications: Mapped[bool] = mapped_column(default=True)
    enable_email_notifications: Mapped[bool] = mapped_column(default=True)
