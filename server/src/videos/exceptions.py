class VideoNotFound(Exception):
    """Raised when video is not found."""

    def __init__(self, message="Video not found"):
        super().__init__(message)


class VideoTitleAlreadyExists(Exception):
    """Raised when video title already exists."""

    def __init__(self, message="Video title already exists"):
        super().__init__(message)


class VideoDataWrongFormat(Exception):
    """Raised when video data has wrong format."""

    def __init__(self, message="Video data has wrong format"):
        super().__init__(message)