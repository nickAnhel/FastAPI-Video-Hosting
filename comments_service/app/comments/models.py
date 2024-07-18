import uuid
from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models import Base


class CommentModel(Base):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(String(1024))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    video_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
