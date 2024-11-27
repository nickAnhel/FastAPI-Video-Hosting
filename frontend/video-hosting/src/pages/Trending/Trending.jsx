import VideoService from "../../service/VideoService";
import VideosGrid from "../../components/VideosGrid/VideosGrid"


function Trending() {
    return (
        <VideosGrid
            fetchVideos={VideoService.getVideos}
            filters={{ order: "views", desc: true }}
        />
    )
}

export default Trending;