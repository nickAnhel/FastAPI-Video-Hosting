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


class CantUploadVideoToS3(Exception):
    """Raised when video can't be uploaded to S3 storage."""

    def __init__(self, message="Can't upload video"):
        super().__init__(message)


class CantUploadPreviewToS3(Exception):
    """Raised when video can't be uploaded to S3 storage."""

    def __init__(self, message="Can't upload preview"):
        super().__init__(message)


class CantDeleteVideoFromS3(Exception):
    """Raised when video can't be deleted from S3 storage."""

    def __init__(self, message="Can't delete video"):
        super().__init__(message)


class CantGetUserID(Exception):
    """Raised when can't get user id from auth service."""

    def __init__(self, message="Can't get user id from auth service"):
        super().__init__(message)


class PermissionDenied(Exception):
    """Raised when permission is denied."""

    def __init__(self, message="Permission denied"):
        super().__init__(message)


class CantDeleteComments(Exception):
    """Raised when can't delete comments."""

    def __init__(self, message="Can't delete comments"):
        super().__init__(message)
