import { useState, useContext, useEffect } from "react";
import "./History.css"

import { Context } from "../../main";
import { AddVideoModalContext, AlertsContext, OptionsContext, ShareModalContext } from "../../App";
import VideoService from "../../service/VideoService";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import VideosList from "../../components/VideosList/VideosList";


function History() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const optionsContext = useContext(OptionsContext);
    const shareModalContext = useContext(ShareModalContext);
    const addVideoContext = useContext(AddVideoModalContext);

    const [refresh, setRefresh] = useState(false);

    const handleShare = (itemId, page) => {
        shareModalContext.setIsActive(true);
        shareModalContext.setLink(`${import.meta.env.VITE_HOST}/${page}/${itemId}`);
    }

    const handleAddToPlaylist = (itemId) => {
        addVideoContext.setActive(true);
        addVideoContext.setVideoId(itemId);
    }

    const handleRemoveFromHistory = async (itemId) => {
        try {
            await VideoService.removeVideoFromHistory(itemId);
            alertsContext.addAlert({
                text: "Successfully removed video from history",
                time: 2000,
                type: "success"
            })
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to removed video from history",
                time: 2000,
                type: "error"
            })
        }

        setRefresh((prev) => !prev);
    }

    useEffect(() => {
        let options = [
            {
                text: "Share",
                iconSrc: "../../../assets/share.svg",
                actionHandler: handleShare,
                params: "videos",
            },
        ]

        if (store.isAuthenticated) {
            options = [
                {
                    text: "Add to playlist",
                    iconSrc: "../../../assets/playlists.svg",
                    actionHandler: handleAddToPlaylist,
                },
                {
                    text: "Remove from history",
                    iconSrc: "../../../assets/remove.svg",
                    actionHandler: handleRemoveFromHistory,
                },
                ...options
            ]
        }

        optionsContext.setOptions(options)
    }, [store.isAuthenticated])


    const handleClearHistory = async () => {
        await VideoService.clearHistory();
        setRefresh((prev) => !prev);
    }

    if (!store.isAuthenticated) {
        return (
            <div className="history-page">
                <Unauthorized />
            </div>
        )
    }

    return (
        <div className="history-page">
            <VideosList fetchVideos={VideoService.getHistory} filters={{ desc: true }} refresh={refresh} />
            <button
                className="clear"
                onClick={handleClearHistory}
            >
                Clear
            </button>
        </div>
    )
}

export default History;