import { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "./VideoDetails.css"

import { Context } from "../../main";
import { AddVideoModalContext, AlertsContext, OptionsContext, ShareModalContext } from "../../App";
import VideoService from "../../service/VideoService";
import Modal from "../Modal/Modal";
import Loader from "../Loader/Loader";
import NotFound from "../NotFound/NotFound";
import CommentsList from "../CommentsList/CommentsList";
import Options from "../Options/Options";


function VideoDetails() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const optionsContext = useContext(OptionsContext);
    const shareModalContext = useContext(ShareModalContext);
    const addVideoContext = useContext(AddVideoModalContext);
    const navigate = useNavigate();

    const [isDeleteModalActive, setIsDeleteModalActive] = useState(false);
    const [isLoadingDelete, setIsLoadingDelete] = useState(false);

    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);
    const [isFirstRender, setIsFirstRender] = useState(true);
    const [isLiked, setIsLiked] = useState(false);
    const [isDisliked, setIsDisliked] = useState(false);

    const [video, setVideo] = useState({});
    const [user, setUser] = useState({});
    const params = useParams();
    const videoId = params.id;

    const [imgSrc, setImgSrc] = useState();

    const handleShare = (itemId, page) => {
        shareModalContext.setIsActive(true);
        shareModalContext.setLink(`${import.meta.env.VITE_HOST}/${page}/${itemId}`);
    }

    const handleAddToPlaylist = (itemId) => {
        addVideoContext.setActive(true);
        addVideoContext.setVideoId(itemId);
    }

    const handleDeleteVideo = async (videoId) => {
        setIsLoadingDelete(true);

        try {
            await VideoService.deleteVideo(videoId);
            alertsContext.addAlert({
                text: "Successfully deleted video",
                time: 2000,
                type: "success"
            })
            navigate("/");
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to delete video",
                time: 2000,
                type: "error"
            })
        }

        setIsLoadingDelete(false);
    }

    const handleDeleteVideoOption = () => {
        setIsDeleteModalActive(true);
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

            if (store.user.id == video.user_id) {
                options = [
                    ...options,
                    {
                        text: "Delete video",
                        iconSrc: "../../../assets/delete.svg",
                        actionHandler: handleDeleteVideoOption,
                    }
                ]
            }
        }

        optionsContext.setOptions(options)
    }, [video])

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);

            try {
                const res = await VideoService.getVideoById(videoId);
                setVideo(res.data);
                setUser(res.data.user);
                setImgSrc(`${import.meta.env.VITE_STORAGE_URL}PPs@${res.data.user.id}?${performance.now()}`)

                if (isFirstRender) {
                    await VideoService.addView(videoId);
                    setIsFirstRender(false);
                }
            } catch (e) {
                console.log(e);
                setIsError(true);
            }

            setIsLoading(false);
            setIsLiked(video?.is_liked);
            setIsDisliked(video?.is_disliked);
        }
        fetchData();
    }, [videoId, isFirstRender])

    const handleLike = async () => {
        if (isLiked) {
            setIsLiked(false);
            const res = await VideoService.unlikeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
        } else {
            setIsLiked(true);
            setIsDisliked(false);
            const res = await VideoService.likeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
        }
    }

    const handleDislike = async () => {
        if (isDisliked) {
            setIsDisliked(false);
            const res = await VideoService.undislikeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
        } else {
            setIsDisliked(true);
            setIsLiked(false);
            const res = await VideoService.dislikeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
        }
    }

    if (isError) {
        return (
            <div className="video-details">
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
        <div className="video-details">
            <div className="video">
                <video
                    src={`${import.meta.env.VITE_STORAGE_URL}VV@${videoId}`}
                    controls
                    loop
                ></video>

                <div className="video-data">
                    <div className="video-header">
                        <div className="video-info">
                            <div className="video-title-wrapper">
                                <div className="video-title">{video.title}</div>
                                <Options itemId={video.id} />
                            </div>

                            <div className="video-stats">
                                <div>{video.views} views</div>
                                <div>{new Date(video.created_at).toLocaleDateString()}</div>
                            </div>
                        </div>

                        <div className="video-desc">{video.description}</div>

                        <Link className="video-author" to={`/channels/${user.id}`}>
                            <img
                                className="video-author-photo"
                                src={imgSrc}
                                onError={() => { setImgSrc("../../../../assets/profile.svg") }}
                                alt="Profile Picture"
                                onClick={() => { setIsModalActive(true) }}
                            />
                            <div className="video-author-info">
                                <div className="video-author-username">{user.username}</div>
                                <div className="video-author-subs-count">{user.subscribers_count} subscriber{user.subscribers_count == 1 ? "" : "s"}</div>
                            </div>

                        </Link>
                    </div>

                    <div className="video-footer">
                        <div className="actions">
                            <button
                                className={isLiked ? "active action left" : "action left"}
                                onClick={handleLike}
                                disabled={!store.isAuthenticated}
                            >
                                <img
                                    className="action-icon"
                                    src="../../../../assets/like.svg"
                                    alt="Like"
                                />
                                {video.likes}
                            </button>
                            <button
                                className={isDisliked ? "active action right" : "action right"}
                                onClick={handleDislike}
                                disabled={!store.isAuthenticated}
                            >
                                <img
                                    className="action-icon"
                                    src="../../../../assets/dislike.svg"
                                    alt="Like"
                                />
                                {video.dislikes}
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            <CommentsList videoId={video.id} />

            <Modal active={isDeleteModalActive} setActive={setIsDeleteModalActive}>
                <div className="delete-video">
                    <h2>Are you sure want to delete this video?</h2>
                    <button
                        className="btn delete"
                        onClick={(e) => handleDeleteVideo(video.id)}
                    >
                        { isLoadingDelete ? <Loader /> : "Delete video" }
                    </button>
                </div>
            </Modal>
        </div>
    )
}

export default VideoDetails;