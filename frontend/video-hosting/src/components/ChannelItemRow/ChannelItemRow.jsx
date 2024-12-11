import { useState } from "react";
import { Link } from "react-router-dom";
import "./ChannelItemRow.css"


function ChannelItemRow({ channel }) {
    const [userProfilePhotoSrc, setUserProfilePhotoSrc] = useState(
        `${import.meta.env.VITE_STORAGE_URL}PPm@${channel.id}?${performance.now()}`
    );

    return (
        <Link className="channel-item-row" to={`/channels/${channel.id}`}>
            <img
                className="channel"
                src={userProfilePhotoSrc}
                onError={() => { setUserProfilePhotoSrc("../../../../assets/profile.svg") }}
                alt=""
            />
        </Link>
    )
}

export default ChannelItemRow;