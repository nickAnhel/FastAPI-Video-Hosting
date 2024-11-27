import { useState, forwardRef } from "react";
import "./VideoItemGrid.css"


const VideoItemGrid = forwardRef((props, ref) => {
    const [userProfilePhotoSrc, setUserProfilePhotoSrc] = useState(
        `${import.meta.env.VITE_STORAGE_URL}PP@${props.video.user_id}?${performance.now()}`
    );

    return (
        <div className="video-item-grid" ref={ref}>
            <img
                className="preview"
                src={`${import.meta.env.VITE_STORAGE_URL}VP@${props.video.id}`}
                alt={props.video.title}
            />
            <div className="info-wrapper">
                <img
                    className="channel"
                    src={userProfilePhotoSrc}
                    onError={() => { setUserProfilePhotoSrc("../../../../assets/profile.svg") }}
                    alt=""
                />
                <div className="info">
                    <div className="title">{props.video.title}</div>
                    <div className="creds">
                        {/* <div className="author">{ props.video.author }</div> */}
                        <div className="author">TEMP</div>
                        <div className="views">{props.video.views} views</div>
                    </div>
                </div>
            </div>
        </div>
    )
});

export default VideoItemGrid;