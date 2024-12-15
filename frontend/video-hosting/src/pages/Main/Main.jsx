import { useContext, useEffect } from "react";
import "./Main.css"

import { Context } from "../../main";
import { OptionsContext, ShareModalContext, AddVideoModalContext } from "../../App";
import VideoService from "../../service/VideoService";
import VideosGrid from "../../components/VideosGrid/VideosGrid"


function Main() {
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
        <div className="main-page">
            <VideosGrid
                fetchVideos={VideoService.getVideos}
                filters={{ order: "created_at", desc: true }}
            />
        </div>

    )
}

export default Main;