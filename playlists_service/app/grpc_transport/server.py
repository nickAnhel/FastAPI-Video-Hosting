from typing import Self
from concurrent.futures import ThreadPoolExecutor
import grpc

from app.grpc_transport import playlist_pb2_grpc
from app.grpc_transport.service import PlaylistGRPCService


class GRPCServer:
    __instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def start(self) -> None:
        self.server = grpc.aio.server(ThreadPoolExecutor(max_workers=10))
        playlist_pb2_grpc.add_PlaylistServicer_to_server(PlaylistGRPCService(), self.server)
        self.server.add_insecure_port("[::]:50051")
        await self.server.start()
        await self.server.wait_for_termination()

    async def stop(self) -> None:
        await self.server.stop(0)
