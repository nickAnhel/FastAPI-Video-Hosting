import uuid
import datetime
from functools import partial
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.users.models import UserModel


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="notifications",
        foreign_keys=[user_id],
    )

    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    channel: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="notificated",
        foreign_keys=[channel_id],
    )

    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"))
    video: Mapped["VideoModel"] = relationship(back_populates="notificated")

    is_read: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc),
    )
