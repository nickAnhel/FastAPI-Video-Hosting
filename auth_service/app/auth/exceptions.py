class UserNotFound(Exception):
    """User not found exception."""

    def __init__(self, username: str):
        super().__init__(f"User with username {username} not found")
