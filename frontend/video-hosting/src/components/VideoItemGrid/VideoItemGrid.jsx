import { useState, forwardRef } from "react";
import { Link } from "react-router-dom";
import "./VideoItemGrid.css"


const VideoItemGrid = forwardRef((props, ref) => {
    const [userProfilePhotoSrc, setUserProfilePhotoSrc] = useState(
        `${import.meta.env.VITE_STORAGE_URL}PPs@${props.video.user_id}?${performance.now()}`
    );

    const formatCreatedAt = (createdAt) => {
        const date = new Date(createdAt)
        return date.toLocaleDateString();
    }

    return (
        <Link to={`/videos/${props.video.id}`} className="video-item-grid" ref={ref}>
            <img
                className="preview"
                src={`${import.meta.env.VITE_STORAGE_URL}VP@${props.video.id}`}
                alt={props.video.title}
            />
            <div className="info-wrapper">
                <Link to={`/channels/${props.video.user_id}`}>
                    <img
                        className="channel"
                        src={userProfilePhotoSrc}
                        onError={() => { setUserProfilePhotoSrc("../../../../assets/profile.svg") }}
                        alt=""
                    />
                </Link>
                <div className="info">
                    <div className="title">{props.video.title}</div>
                    <div className="creds">
                        <Link className="author" to={`/channels/${props.video.user_id}`}>{ props.video.user.username }</Link> •
                        <div className="views">{props.video.views} views</div> •
                        <div>{formatCreatedAt(props.video.created_at)}</div>
                    </div>
                </div>
            </div>
        </Link>
    )
});

export default VideoItemGrid;