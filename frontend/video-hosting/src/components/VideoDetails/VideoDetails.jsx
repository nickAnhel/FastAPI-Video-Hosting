import { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import "./VideoDetails.css"

import { Context } from "../../main";
import VideoService from "../../service/VideoService";
import Loader from "../Loader/Loader";
import NotFound from "../NotFound/NotFound";
import CommentsList from "../CommentsList/CommentsList";
import ChannelItemList from "../ChannelItemList/ChannelItemList";


function VideoDetails() {
    const { store } = useContext(Context);

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
            const res = await VideoService.unlikeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            })); setIsLiked(false);
            setIsLiked(false);
        } else {
            const res = await VideoService.likeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
            setIsLiked(true);
            setIsDisliked(false);
        }
    }

    const handleDislike = async () => {
        if (isDisliked) {
            const res = await VideoService.undislikeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
            setIsDisliked(false);
        } else {
            const res = await VideoService.dislikeVideo(video.id);
            setVideo((prev) => ({
                ...prev,
                likes: res.data.likes,
                dislikes: res.data.dislikes,
            }));
            setIsDisliked(true);
            setIsLiked(false);
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
                    // poster={`${import.meta.env.VITE_STORAGE_URL}VP@${videoId}`}
                    controls
                    loop
                ></video>

                <div className="video-data">
                    <div className="video-header">
                        <div className="video-info">
                            <div className="video-title">{video.title}</div>
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
                                <div className="video-author-subs-count">{ user.subscribers_count } subscriber{ user.subscribers_count == 1 ? "" : "s" }</div>
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
                                {video.likes} Like{video.likes == 1 ? "" : "s"}
                            </button>
                            <button
                                className={isDisliked ? "active action right" : "action right" }
                                onClick={handleDislike}
                                disabled={!store.isAuthenticated}
                            >
                                {video.dislikes} Dislike{video.dislikes == 1 ? "" : "s"}
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            <CommentsList videoId={video.id} />
        </div>
    )
}

export default VideoDetails;