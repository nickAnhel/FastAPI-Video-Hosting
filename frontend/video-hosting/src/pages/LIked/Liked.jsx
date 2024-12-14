import { useContext } from "react";
import "./Liked.css"

import { Context } from "../../main";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import VideoService from "../../service/VideoService";
import VideosList from "../../components/VideosList/VideosList";


function Liked() {
    const { store } = useContext(Context);

    if (!store.isAuthenticated) {
        return (
            <div className="liked-page">
                <Unauthorized />
            </div>
        )
    }

    return (
        <div className="liked-page">
            <VideosList fetchVideos={VideoService.getLiked} filters={{ desc: true }} />
        </div>
    )
}

export default Liked;