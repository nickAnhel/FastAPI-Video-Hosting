import "./Main.css"

import VideoService from "../../service/VideoService";
import VideosGrid from "../../components/VideosGrid/VideosGrid"


function Main() {
    return (
        <div className="main-page">
            <VideosGrid
                fetchVideos={VideoService.getVideos}
                filters={{ order: "created_at", desc: true }}
            />
        </div>

    )
}

export default Main;