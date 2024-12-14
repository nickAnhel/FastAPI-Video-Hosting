import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class PlaylistModel(Base):
    __tablename__ = "playlists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    private: Mapped[bool] = mapped_column(default=False)
    videos_count: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="playlists")  # type: ignore

    videos: Mapped[list["VideoModel"]] = relationship(  # type: ignore
        back_populates="playlists",
        secondary="playlist_video",
    )


class PlaylistVideoM2M(Base):
    __tablename__ = "playlist_video"

    playlist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("playlists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        primary_key=True,
    )
