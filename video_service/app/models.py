import uuid
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    # id: Mapped[int] = mapped_column(primary_key=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,)

    def __repr__(self) -> str:
        res = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                res.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(res)})"
