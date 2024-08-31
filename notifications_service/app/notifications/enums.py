from enum import Enum


class NotificationTypes(Enum):
    NEW_VIDEO = "new_video"
    SUBSCRIPTION = "subscription"
    COMMENT = "comment"

    def __str__(self) -> str:
        return self.value
