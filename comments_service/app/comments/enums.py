from enum import Enum


class CommentOrder(str, Enum):
    ID = "id"
    LIKES = "likes"
    DISLIKES = "dislikes"
    CREATED_AT = "created_at"

    def __str__(self) -> str:
        return self.value
