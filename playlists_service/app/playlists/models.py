import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from app.models import Base


class PlaylistModel(Base):
    __tablename__ = "playlists"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    video_ids: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID(as_uuid=True)))
    private: Mapped[bool] = mapped_column(default=False)
