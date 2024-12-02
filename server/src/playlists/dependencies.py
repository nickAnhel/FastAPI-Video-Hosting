from src.playlists.service import PlaylistService


def get_playlists_service() -> PlaylistService:
    return PlaylistService()
