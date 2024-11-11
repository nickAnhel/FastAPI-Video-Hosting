from uuid import UUID

from app.grpc_transport.playlist_pb2_grpc import PlaylistServicer
from app.grpc_transport.playlist_pb2 import PlaylistCreateRequest, PlaylistCreateResponse
from app.playlists.service import PlaylistService
from app.playlists.schemas import PlaylistCreate


class PlaylistGRPCService(PlaylistServicer):
    async def create(
        self,
        request: PlaylistCreateRequest,
        context,
    ) -> PlaylistCreateResponse:
        print("Take request: ", request)

        await PlaylistService().create_playlist(
            user_id=UUID(request.user_id),
            data=PlaylistCreate(
                title=request.title,
                description="",
                video_ids=[],
                private=request.private,
            ),
        )
        return PlaylistCreateResponse(success=True)
