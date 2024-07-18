from enum import Enum


class UserOrder(str, Enum):
    ID = "id"

    def __str__(self) -> str:
        return self.value
