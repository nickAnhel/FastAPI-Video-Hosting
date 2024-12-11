import "./Liked.css"

import VideoService from "../../service/VideoService";
import VideosList from "../../components/VideosList/VideosList";


function Liked() {
    return (
        <div className="liked-page">
            <VideosList fetchVideos={VideoService.getLiked} filters={{ desc: true }} />
        </div>
    )
}

export default Liked;