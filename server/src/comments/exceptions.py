class CommentNotFound(Exception):
    """Raised when comment is not found."""

    def __init__(self, message="Comment not found"):
        super().__init__(message)


class CommentContentWrongFormat(Exception):
    """Raised when comment content has wrong format."""

    def __init__(self, message="Comment content has wrong format"):
        super().__init__(message)
