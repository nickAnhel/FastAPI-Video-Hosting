class CantSendNotification(Exception):
    """Raise when can't send notification."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
