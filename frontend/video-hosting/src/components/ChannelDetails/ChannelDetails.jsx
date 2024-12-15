import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import "./ChannelDetails.css"

import { Context } from "../../main";
import { AddVideoModalContext, AlertsContext, OptionsContext, ShareModalContext } from "../../App";
import UserService from "../../service/UserService";
import VideoService from "../../service/VideoService";
import PlaylistService from "../../service/PlaylistService";

import Loader from "../Loader/Loader";
import NotFound from "../NotFound/NotFound";
import VideosGrid from "../VideosGrid/VideosGrid";
import ChannelsList from "../ChannelsList/ChannelsList";
import SocialLink from "../SocialLink/SocialLink";
import PlaylistsList from "../PlaylistsList/PlaylistsList";


function ChannelDetails() {
    const { store } = useContext(Context)
    const alertsContext = useContext(AlertsContext);
    const optionsContext = useContext(OptionsContext);
    const shareModalContext = useContext(ShareModalContext);
    const addVideoContext = useContext(AddVideoModalContext);
    const params = useParams();

    const [refresh, setRefresh] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingSub, setIsLoadingSub] = useState(false);
    const [isError, setIsError] = useState(false);

    const [channel, setChannel] = useState({});
    const [isSubscribed, setIsSubsctribed] = useState(null);
    const [subsCount, setSubsCount] = useState();
    const [socialLinks, setSocialLinks] = useState([]);
    const channelId = params.id;

    const [tab, setTab] = useState(1);

    const [imgSrc, setImgSrc] = useState(null);

    const handleShare = (itemId, page) => {
        shareModalContext.setIsActive(true);
        shareModalContext.setLink(`${import.meta.env.VITE_HOST}/${page}/${itemId}`);
    }

    const handleAddToPlaylist = (itemId) => {
        addVideoContext.setActive(true);
        addVideoContext.setVideoId(itemId);
    }

    const handleDeletePlaylist = async (itemId) => {
        try {
            await PlaylistService.deletePlylistById(itemId);
            setRefresh((prev) => !prev);
            alertsContext.addAlert({
                text: "Playlist deleted successfully",
                time: 2000,
                type: "success"
            })
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to delete playlist",
                time: 2000,
                type: "error"
            })
        }
    }

    useEffect(() => {
        let options = []

        if (store.isAuthenticated && tab == 1) {
            options = [
                {
                    text: "Add to playlist",
                    iconSrc: "../../../assets/playlists.svg",
                    actionHandler: handleAddToPlaylist,
                },
                {
                    text: "Share",
                    iconSrc: "../../../assets/share.svg",
                    actionHandler: handleShare,
                    params: "videos",
                },
            ]

        } else if (store.isAuthenticated && tab == 2) {
            options = [
                {
                    text: "Share",
                    iconSrc: "../../../assets/share.svg",
                    actionHandler: handleShare,
                    params: "playlists",
                }
            ]
            if (store.user.id == channelId) {
                options = [
                    {
                        text: "Delete playlist",
                        iconSrc: "../../../assets/delete.svg",
                        actionHandler: handleDeletePlaylist,
                    },
                    ...options,
                ]
            }
        }

        optionsContext.setOptions(options)
    }, [channelId, tab])

    useEffect(() => {
        const fetchData = async () => {
            setTab(1);
            setIsLoading(true);

            try {
                const res = await UserService.getUserById(channelId);
                setChannel(res.data);
                setImgSrc(`${import.meta.env.VITE_STORAGE_URL}PPl@${channelId}?${performance.now()}`);
                setIsSubsctribed(res.data.is_subscribed);
                setSubsCount(res.data.subscribers_count);
                setSocialLinks(res.data.social_links);
            } catch (e) {
                console.log(e);
                setIsError(true);
            }

            setIsLoading(false);
        }
        fetchData();
    }, [channelId])

    const handleSubscribe = async () => {
        setIsLoadingSub(true);

        try {
            await UserService.subscribeToUser(channel.id);
            setIsSubsctribed(true);
            setSubsCount((prev) => prev + 1);
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to subscribe to channel",
                time: 2000,
                type: "error"
            })
            return;
        }

        setIsLoadingSub(false);
        alertsContext.addAlert({
            text: "Successfully subscribed to channel",
            time: 2000,
            type: "success"
        })
    }

    const handleUnsubscribe = async () => {
        setIsLoadingSub(true);

        try {
            await UserService.unsubscribFromuser(channel.id);
            setIsSubsctribed(false);
            setSubsCount((prev) => prev - 1);
        } catch (e) {
            alertsContext.addAlert({
                text: "Failed to unsubscribe from channel",
                time: 2000,
                type: "error"
            })
            console.log(e);
        }

        setIsLoadingSub(false);
        alertsContext.addAlert({
            text: "Successfully unsubscribed from channel",
            time: 2000,
            type: "success"
        })
    }

    if (isError) {
        return (
            <div className="channel-details">
                <NotFound />
            </div>
        )
    }

    if (isLoading) {
        return (
            <div className="video-details">
                <Loader />
            </div>
        )
    }

    return (
        <div className="channel-details">
            <div className="channel-info">
                <img
                    className="channel-pic"
                    src={imgSrc}
                    onError={() => { setImgSrc("../../../../assets/profile.svg") }}
                    alt={channel.username}
                />

                <div className="channel-data">
                    <div>
                        <div className="channel-username">{channel.username}</div>
                        <div className="channel-subs-count">{subsCount} subscriber{subsCount == 1 ? "" : "s"}</div>
                    </div>
                    <div className="channel-about">{channel.about}</div>
                    <div className="channel-social-links">
                        {
                            socialLinks.map((link, index) => {
                                return <SocialLink key={index} link={link} />
                            })
                        }
                    </div>
                </div>

                <div className="subscribe-btn">
                    {
                        store.user.id != channel.id && (
                            isSubscribed ?
                                <button
                                    className="btn unsubscribe"
                                    onClick={handleUnsubscribe}
                                >
                                    {isLoadingSub ? <Loader /> : "Unsubscribe"}
                                </button>
                                :
                                <button
                                    className="btn"
                                    onClick={handleSubscribe}
                                    disabled={!store.isAuthenticated}
                                >
                                    {isLoadingSub ? <Loader /> : "Subscribe"}
                                </button>
                        )

                    }
                </div>

            </div>

            <div className="tabs">
                <div
                    className={tab == 1 ? "tab current" : "tab"}
                    onClick={() => setTab(1)}
                >Videos</div>
                <div
                    className={tab == 2 ? "tab current" : "tab"}
                    onClick={() => setTab(2)}
                >Playlists</div>
                <div
                    className={tab == 3 ? "tab current" : "tab"}
                    onClick={() => setTab(3)}
                >Subscriptions</div>
            </div>

            <div className="content">
                {
                    tab == 1 &&
                    <VideosGrid fetchVideos={VideoService.getVideos} filters={{ user_id: channel.id, order: "created_at", desc: true }} />
                }
                {
                    tab == 2 &&
                    <PlaylistsList filters={{ owner_id: channel.id }} refresh={refresh} />
                }
                {
                    tab == 3 &&
                    <ChannelsList fetchChannels={UserService.getSubsctiptions} filters={{ user_id: channel.id }} />
                }
            </div>
        </div>
    )
}

export default ChannelDetails;