from app.videos.repository import VideoRepository
from app.videos.scemas import VideoCreate, VideoGet
from app.videos.exceptions import VideoNotFound


class VideoService:
    def __init__(self, repository: VideoRepository):
        self.repository = repository

    async def create_video(
        self,
        data: VideoCreate,
    ) -> VideoGet:
        video_model = await self.repository.create(data=data.model_dump())
        return VideoGet.model_validate(video_model)

    async def get_video(
        self,
        **filters,
    ) -> VideoGet | None:
        video = await self.repository.get_single(**filters)

        if not video:
            raise VideoNotFound()

        return VideoGet.model_validate(video)


    async def get_videos(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[VideoGet]:
        videos = await self.repository.get_multi(order=order, offset=offset, limit=limit)
        return [VideoGet.model_validate(video) for video in videos]


    async def delete_video(
        self,
        **filters,
    ) -> None:
        await self.repository.delete(**filters)