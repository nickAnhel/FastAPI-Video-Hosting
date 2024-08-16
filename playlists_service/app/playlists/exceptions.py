class CantGetUserID(Exception):
    """Raised when can't get user id from auth service."""

    def __init__(self, message="Can't get user id from auth service"):
        super().__init__(message)


class PermissionDenied(Exception):
    """Raised when permission is denied."""

    def __init__(self, message="Permission denied"):
        super().__init__(message)


class PlaylistNotFound(Exception):
    """Raised when playlist is not found."""

    def __init__(self, message="Playlist not found"):
        super().__init__(message)


class PlaylistTitleAlreadyExists(Exception):
    """Raised when playlist with this title already exists."""

    def __init__(self, message="Playlist with this title already exists"):
        super().__init__(message)


class PlaylistDoesNotContainVideo(Exception):
    """Raised when playlist with this title already exists."""

    def __init__(self, message="Playlist does not contain video"):
        super().__init__(message)
