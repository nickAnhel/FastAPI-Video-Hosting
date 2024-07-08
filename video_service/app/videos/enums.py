from enum import Enum


class VideoOrder(str, Enum):
    ID: str = "id"
    TITLE: str = "title"
    VIEWS: str = "views"
    LIKES: str = "likes"
    DISLIKES: str = "dislikes"
    CREATED_AT: str = "created_at"

    def __str__(self) -> str:
        return self.value
