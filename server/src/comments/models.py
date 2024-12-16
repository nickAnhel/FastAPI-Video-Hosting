import uuid
import datetime
from functools import partial
from sqlalchemy import ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String(1024))

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="comments")  # type: ignore

    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"))
    video: Mapped["VideoModel"] = relationship(back_populates="comments")  # type: ignore

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc),
    )

    @property
    def content_ellipsis(self) -> str:
        if len(self.content) < 100:
            return self.content

        return " ".join(self.content.split()[:5]) + "..."
