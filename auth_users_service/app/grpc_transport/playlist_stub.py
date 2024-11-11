import grpc
from app.grpc_transport.playlist_pb2_grpc import PlaylistStub
from app.grpc_transport.playlist_pb2 import PlaylistCreateRequest

from app.users.schemas import Playlist
from app.config import settings


class PlaylistGRPCStub:
    def create(self, data: Playlist) -> bool:
        with grpc.insecure_channel(settings.services.playlists_service_url) as channel:
            stub = PlaylistStub(channel)
            return stub.create(
                PlaylistCreateRequest(
                    user_id=str(data.user_id),
                    title=data.title,
                    private=data.private,
                ),
            ).success


plylist_grpc_stub = PlaylistGRPCStub()
