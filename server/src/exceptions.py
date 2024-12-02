class PermissionDenied(Exception):
    """Raised when permission is denied."""

    def __init__(self, message="Permission denied"):
        super().__init__(message)
