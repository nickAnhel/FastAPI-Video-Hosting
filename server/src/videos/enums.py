from enum import Enum


class VideoOrder(str, Enum):
    ID = "id"
    TITLE = "title"
    VIEWS = "views"
    LIKES = "likes"
    DISLIKES = "dislikes"
    CREATED_AT = "created_at"

    def __str__(self) -> str:
        return self.value


class HistoryOrder(str, Enum):
    ID = "id"
    WATCHED_AT = "watched_at"

    def __str__(self) -> str:
        return self.value
