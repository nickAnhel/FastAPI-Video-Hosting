class CantUploadFileToStorage(Exception):
    """Raised when cant upload file to S3 Storage."""

    def __init__(self, message="Can't upload file to S3 Storage"):
        super().__init__(message)


class CantDeleteFileFromStorage(Exception):
    """Raised when cant delete file from S3 Storage."""

    def __init__(self, message="Can't delete file from S3 Storage"):
        super().__init__(message)
