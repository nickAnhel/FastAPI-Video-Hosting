import { useContext, useEffect } from "react";
import "./Trending.css"

import { Context } from "../../main";
import { AddVideoModalContext, OptionsContext, ShareModalContext } from "../../App";
import VideoService from "../../service/VideoService";
import VideosGrid from "../../components/VideosGrid/VideosGrid"


function Trending() {
    const { store } = useContext(Context);
    const optionsContext = useContext(OptionsContext);
    const shareModalContext = useContext(ShareModalContext);
    const addVideoContext = useContext(AddVideoModalContext);

    const handleShare = (itemId, page) => {
        shareModalContext.setIsActive(true);
        shareModalContext.setLink(`${import.meta.env.VITE_HOST}/${page}/${itemId}`);
    }

    const handleAddToPlaylist = (itemId) => {
        addVideoContext.setActive(true);
        addVideoContext.setVideoId(itemId);
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
    }, [store.isAuthenticated])

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