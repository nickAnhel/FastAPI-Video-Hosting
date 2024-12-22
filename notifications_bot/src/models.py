import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        res = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                res.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(res)})"


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    email: Mapped[str] = mapped_column(unique=True)
    is_verified_email: Mapped[bool] = mapped_column(default=False)

    telegram_username: Mapped[str | None] = mapped_column(unique=True)
    is_verified_telegram: Mapped[bool] = mapped_column(default=False)

    about: Mapped[str] = mapped_column(String(1024), default="")
    social_links: Mapped[list[str]] = mapped_column(ARRAY(String))

    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    subscribers_count: Mapped[int] = mapped_column(default=0)
