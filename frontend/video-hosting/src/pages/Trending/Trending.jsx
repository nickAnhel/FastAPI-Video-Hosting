import "./Trending.css"

import VideoService from "../../service/VideoService";
import VideosGrid from "../../components/VideosGrid/VideosGrid"


function Trending() {
    return (
        <div className="trending-page">
            <VideosGrid
                fetchVideos={VideoService.getVideos}
                filters={{ order: "views", desc: true }}
            />
        </div>
    )
}

export default Trending;