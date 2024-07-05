class VideoNotFound(Exception):
    """Raised when video is not found"""
    def __init__(self, message="Video not found"):
        super().__init__(message)