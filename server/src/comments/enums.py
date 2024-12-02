from enum import Enum


class CommentOrder(str, Enum):
    ID = "id"
    CREATED_AT = "created_at"

    def __str__(self) -> str:
        return self.value
