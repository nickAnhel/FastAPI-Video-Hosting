import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from src.models import Base


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    subscriber_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    subscribed_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    about: Mapped[str] = mapped_column(String(1024), default="")
    social_links: Mapped[list[str]] = mapped_column(ARRAY(String))

    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    subscribers_count: Mapped[int] = mapped_column(default=0)

    subscribers: Mapped[list["UserModel"]] = relationship(
        back_populates="subscribed",
        secondary="user_subscriptions",
        primaryjoin=(id == UserSubscription.subscribed_id),
        secondaryjoin=(id == UserSubscription.subscriber_id),
    )
    subscribed: Mapped[list["UserModel"]] = relationship(
        back_populates="subscribers",
        secondary="user_subscriptions",
        primaryjoin=(id == UserSubscription.subscriber_id),
        secondaryjoin=(id == UserSubscription.subscribed_id),
    )

    settings: Mapped["SettingsModel"] = relationship(back_populates="user")  # type: ignore
    created_videos: Mapped[list["VideoModel"]] = relationship(back_populates="user")  # type: ignore
    playlists: Mapped[list["PlaylistModel"]] = relationship(back_populates="user")  # type: ignore
    comments: Mapped[list["CommentModel"]] = relationship(back_populates="user")  # type: ignore

    liked_videos: Mapped[list["VideoModel"]] = relationship(  # type: ignore
        back_populates="liked_users",
        secondary="user_video_likes",
    )
    disliked_videos: Mapped[list["VideoModel"]] = relationship(  # type: ignore
        back_populates="disliked_users",
        secondary="user_video_dislikes",
    )
    watched_videos: Mapped[list["VideoModel"]] = relationship(  # type: ignore
        back_populates="watched_users",
        secondary="user_video_history",
    )