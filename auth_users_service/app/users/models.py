from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from app.models import Base


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    about: Mapped[str] = mapped_column(String(1024), default="")
    social_links: Mapped[list[str]] = mapped_column(ARRAY(String))

    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
