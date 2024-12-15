import { useEffect, useContext } from "react";
import "./Subscriptions.css"

import { Context } from "../../main";
import { AddVideoModalContext, OptionsContext, ShareModalContext } from "../../App";
import VideoService from "../../service/VideoService";
import UserService from "../../service/UserService";
import Unauthorized from "../Unauthorized/Unauthorized";
import ChannelsRow from "../ChannelsRow/ChannelsRow";
import VideosGrid from "../VideosGrid/VideosGrid";


function Subscriptions() {
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
            <div className="subcriptions">
                <Unauthorized />
            </div>
        )
    }

    return (
        <div className="subcriptions">
            <ChannelsRow fetchChannels={UserService.getSubsctiptions} filters={{ user_id: store.user.id }} />
            <VideosGrid fetchVideos={VideoService.getSubscriptions} filters={{order: "created_at", desc: true}}/>
        </div>
    )
}

export default Subscriptions;