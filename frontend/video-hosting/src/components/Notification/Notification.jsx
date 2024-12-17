import { useState, forwardRef } from "react"
import { Link } from "react-router-dom"
import "./Notification.css"

import NotificationsService from "../../service/NotificationsService"


const Notification = forwardRef((props, ref) => {
    const [imgSrc, setImgSrc] = useState(`${import.meta.env.VITE_STORAGE_URL}PPm@${props.notification.channel.id}?${performance.now()}`);

    const handleDelete = async (event) => {
        event.preventDefault();
        event.stopPropagation();

        try {
            await NotificationsService.deleteNotificationById(props.notification.id);
            props.refresh();
        } catch (e) {
            console.log(e);
        }
    }

    return (
        <Link
            ref={ref}
            className="notification"
            to={`/videos/${props.notification.video.id}`}
            onClick={() => props.setOpen(false)}
        >
            <Link to={`/channels/${props.notification.channel.id}`}>
                <img
                    className="channel"
                    src={imgSrc}
                    alt={props.notification.channel.username}
                    onError={e => setImgSrc("../../../../assets/profile.svg")}
                />

            </Link>

            <div className="notification-text">
                <strong>{props.notification.channel.username}</strong> published new video <strong>{props.notification.video.title}</strong>
            </div>

            <img
                className="notification-delete"
                src="../../../../assets/clear.svg"
                alt="Delete Notification"
                onClick={handleDelete}
            />
        </Link>
    )
})

export default Notification;