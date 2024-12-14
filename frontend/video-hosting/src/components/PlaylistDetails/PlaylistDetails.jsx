import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./PlaylistDetails.css"

import PlaylistService from "../../service/PlaylistService";
import VideoService from "../../service/VideoService";
import NotFound from "../NotFound/NotFound";
import Loader from "../Loader/Loader";
import VideosList from "../../components/VideosList/VideosList";


function PlaylistDetails() {
    const params = useParams();
    const playlistId = params.id;

    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);
    const [playlist, setPlaylist] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);

            try {
                const res = await PlaylistService.getPlaylistById(playlistId);
                setPlaylist(res.data);
            } catch (e) {
                console.log(e);
                setIsError(true);
            }

            setIsLoading(false);
        }
        fetchData();
    }, [playlistId])

    if (isError) {
        return <NotFound />
    }

    if (isLoading) {
        return (
            <div className="playlist-details">
                <Loader />
            </div>
        )
    }

    return (
        <div className="playlist-details">
            <div className="playlist-info">
                <h2 className="playlist-title">{playlist.title}</h2>
                <div className="playlist-desc">{playlist.description}</div>
                <div className="playlist-videos-count">{playlist.videos_count} video{playlist.videos_count == 1 ? "" : "s"}</div>
            </div>

            <VideosList fetchVideos={VideoService.getPlaylistVideos} filters={{ playlist_id: playlist.id }} />
        </div>
    )
}

export default PlaylistDetails;