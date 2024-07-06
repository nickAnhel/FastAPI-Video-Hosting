class VideoNotFound(Exception):
    """Raised when video is not found"""

    def __init__(self, message="Video not found"):
        super().__init__(message)


class CantUploadVideoToS3(Exception):
    """Raised when video can't be uploaded to S3 storage"""

    def __init__(self, message="Can't upload video"):
        super().__init__(message)


class CantDeleteVideoFromS3(Exception):
    """Raised when video can't be deleted from S3 storage"""

    def __init__(self, message="Can't delete video"):
        super().__init__(message)
