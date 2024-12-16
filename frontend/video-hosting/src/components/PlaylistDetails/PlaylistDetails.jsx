import { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./PlaylistDetails.css"

import { Context } from "../../main";
import { AddVideoModalContext, AlertsContext, OptionsContext, ShareModalContext } from "../../App";
import PlaylistService from "../../service/PlaylistService";
import VideoService from "../../service/VideoService";

import NotFound from "../NotFound/NotFound";
import Loader from "../Loader/Loader";
import VideosList from "../../components/VideosList/VideosList";


function PlaylistDetails() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const optionsContext = useContext(OptionsContext);
    const shareModalContext = useContext(ShareModalContext);
    const addVideoContext = useContext(AddVideoModalContext);
    const navigate = useNavigate();

    const params = useParams();
    const playlistId = params.id;

    const [refresh, setRefresh] = useState(false);

    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);
    const [playlist, setPlaylist] = useState({});

    const handleShare = (itemId, page) => {
        shareModalContext.setIsActive(true);
        shareModalContext.setLink(`${import.meta.env.VITE_HOST}/${page}/${itemId}`);
    }

    const handleAddToPlaylist = (itemId) => {
        addVideoContext.setActive(true);
        addVideoContext.setVideoId(itemId);
    }

    const handleRemoveFromPlaylist = async (itemId) => {
        try {
            await PlaylistService.removeVideoFromPlaylist(itemId, playlist.id);
            setRefresh((prev) => !prev);
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to remove video from playlist",
                time: 2000,
                type: "error"
            })
        }
    }

    useEffect(() => {
        let options = [
            {
                text: "Share",
                iconSrc: "../../../assets/share.svg",
                actionHandler: handleShare,
                params: "videos",
            }
        ]

        if (store.isAuthenticated) {
            if (store.user.id == playlist.user_id) {
                options = [
                    {
                        text: "Remove from playlist",
                        iconSrc: "../../../assets/remove.svg",
                        actionHandler: handleRemoveFromPlaylist,
                    },
                    ...options,
                ]
            }

            options = [
                {
                    text: "Add to playlist",
                    iconSrc: "../../../assets/playlists.svg",
                    actionHandler: handleAddToPlaylist,
                },
                ...options
            ]
        }

        optionsContext.setOptions(options)
    }, [playlist])

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

    const handleDelete = async () => {
        try {
            await PlaylistService.deletePlylistById(playlist.id);
            alertsContext.addAlert({
                text: "Playlist successfully deleted",
                time: 2000,
                type: "success"
            })
            navigate("/playlists")
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to delete playlist",
                time: 2000,
                type: "error"
            })
        }
    }

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
                <div className="title-wrapper">
                    <h2 className="playlist-title">{playlist.title}</h2>

                    {
                        store.isAuthenticated && store.user.id == playlist.user_id &&
                        <img
                            src="../../../assets/delete.svg"
                            alt="Delete playlist"
                            onClick={handleDelete}
                        />
                    }
                </div>
                <div className="playlist-desc">{playlist.description}</div>
                <div className="playlist-videos-count">{playlist.videos_count} video{playlist.videos_count == 1 ? "" : "s"}</div>
            </div>

            <div className="playlist-videos">
                <VideosList fetchVideos={VideoService.getPlaylistVideos} filters={{ playlist_id: playlist.id }} refresh={refresh} />
            </div>
        </div>
    )
}

export default PlaylistDetails;