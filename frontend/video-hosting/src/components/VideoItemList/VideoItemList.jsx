import { useState, forwardRef } from "react";
import { Link } from "react-router-dom";
import "./VideoItemList.css"


const VideoItemList = forwardRef((props, ref) => {
    const [userProfilePhotoSrc, setUserProfilePhotoSrc] = useState(
        `${import.meta.env.VITE_STORAGE_URL}PPs@${props.video.user_id}?${performance.now()}`
    );

    const formatCreatedAt = (createdAt) => {
        const date = new Date(createdAt)
        return date.toLocaleDateString();
    }

    return (
        <Link to={`/videos/${props.video.id}`} className="video-item-list" ref={ref}>
            <img
                className="preview"
                src={`${import.meta.env.VITE_STORAGE_URL}VP@${props.video.id}`}
                alt={props.video.title}
            />
            <div className="info">
                <div className="title">{props.video.title}</div>
                <Link className="author" to={`/channels/${props.video.user_id}`}>
                    <img
                        className="channel"
                        src={userProfilePhotoSrc}
                        onError={() => { setUserProfilePhotoSrc("../../../../assets/profile.svg") }}
                        alt=""
                    />
                    <div>{ props.video.user.username }</div>
                </Link>
                <div className="description">
                    {props.video.description}
                </div>
                <div className="stats">
                    <div>{props.video.views} view{props.video.views == 1 ? "": "s"}</div> •
                    <div>{formatCreatedAt(props.video.created_at)}</div> •
                    <div>{props.video.likes} like{props.video.likes == 1 ? "": "s"}</div>
                </div>
            </div>
        </Link>
    )
});

export default VideoItemList;