from datetime import datetime
from sqlalchemy import Column, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models import Base


class VideoModel(Base):
    __tablename__ = "videos"

    title: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    views: Mapped[int] = mapped_column(default=0)
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)

    user_id = Column(UUID(as_uuid=True))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
