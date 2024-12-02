class PlaylistNotFound(Exception):
    def __init__(self, message="Playlist not found"):
        super().__init__(message)


class CantRemoveVideoFromPlaylist(Exception):
    def __init__(self, message="Playlist does not contain video"):
        super().__init__(message)


class CantAddVideoToPlaylist(Exception):
    def __init__(self, message="Can't add video to playlist"):
        super().__init__(message)
