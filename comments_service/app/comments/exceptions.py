class CantGetUserID(Exception):
    """Raised when can't get user id from auth service."""

    def __init__(self, message="Can't get user id from auth service"):
        super().__init__(message)


class PermissionDenied(Exception):
    """Raised when permission is denied."""

    def __init__(self, message="Permission denied"):
        super().__init__(message)


class CommentNotFound(Exception):
    """Raised when comment is not found."""

    def __init__(self, message="Comment not found"):
        super().__init__(message)
