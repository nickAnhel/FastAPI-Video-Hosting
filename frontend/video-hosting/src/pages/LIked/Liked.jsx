import { useContext, useEffect } from "react";
import "./Liked.css"

import { Context } from "../../main";
import { AddVideoModalContext, OptionsContext, ShareModalContext } from "../../App";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import VideoService from "../../service/VideoService";
import VideosList from "../../components/VideosList/VideosList";


function Liked() {
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