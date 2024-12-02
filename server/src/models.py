from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        res = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                res.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(res)})"
