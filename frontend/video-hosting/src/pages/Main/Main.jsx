import VideoService from "../../service/VideoService";
import VideosGrid from "../../components/VideosGrid/VideosGrid"


function Main() {
    return (
        <VideosGrid
            fetchVideos={VideoService.getVideos}
            filters={{ order: "created_at" }}
        />

    )
}

export default Main;