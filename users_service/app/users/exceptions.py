class UserNotFound(Exception):
    """User not found exception."""

    def __init__(self, message="User not found"):
        super().__init__(message)


class InvalidAuthToken(Exception):
    """Invalid authorization token exception."""

    def __init__(self, message="Invalid authorization token"):
        super().__init__(message)
