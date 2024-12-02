import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class VideoModel(Base):
    __tablename__ = "videos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    views: Mapped[int] = mapped_column(default=0)
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="created_videos")  # type: ignore

    comments: Mapped[list["CommentModel"]] = relationship(back_populates="video")  # type: ignore

    playlists: Mapped[list["PlaylistModel"]] = relationship(  # type: ignore
        back_populates="videos",
        secondary="playlist_video",
    )

    liked_users: Mapped[list["UserModel"]] = relationship(  # type: ignore
        back_populates="liked_videos",
        secondary="user_video_likes",
    )
    disliked_users: Mapped[list["UserModel"]] = relationship(  # type: ignore
        back_populates="disliked_videos",
        secondary="user_video_dislikes",
    )
    watched_users: Mapped[list["UserModel"]] = relationship(  # type: ignore
        back_populates="watched_videos",
        secondary="user_video_history",
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class LikesModel(Base):
    __tablename__ = "user_video_likes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        primary_key=True,
    )


class DislikesModel(Base):
    __tablename__ = "user_video_dislikes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        primary_key=True,
    )


class WatchHistoryModel(Base):
    __tablename__ = "user_video_history"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        primary_key=True,
    )
