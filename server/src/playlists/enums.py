from enum import Enum


class PlaylistOrder(str, Enum):
    ID = "id"
    TITLE = "title"

    def __str__(self) -> str:
        return self.value
