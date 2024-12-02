from enum import Enum


class UserOrder(str, Enum):
    ID = "id"
    SUBSCRIBERS_COUNT = "subscribers_count"

    def __str__(self) -> str:
        return self.value
