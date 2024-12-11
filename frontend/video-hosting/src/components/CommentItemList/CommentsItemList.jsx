import { useState, useContext, forwardRef } from "react";
import { Link } from "react-router-dom";
import "./CommentItemList.css"

import { Context } from "../../main";
import { AlertsContext } from "../../App";
import CommentService from "../../service/CommentService";


const CommentItemList = forwardRef((props, ref) => {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const [userProfilePhotoSrc, setUserProfilePhotoSrc] = useState(
        `${import.meta.env.VITE_STORAGE_URL}PPs@${props.comment.user.id}?${performance.now()}`
    );

    const handleCommentDelete = async () => {
        try {
            await CommentService.deleteComment(props.comment.id);
            props.removeComment(props.comment.id);
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to delete comment",
                time: 2000,
                type: "error"
            })
        }
    }

    return (
        <div className="comment-item-list" ref={ref}>
            <Link to={`/channels/${props.comment.user.id}`}>
                <img
                    className="comment-author-photo"
                    src={userProfilePhotoSrc}
                    onError={() => { setUserProfilePhotoSrc("../../../../assets/profile.svg") }}
                />
            </Link>

            <div className="comment-data">
                <div className="comment-header">
                    <Link to={`/channels/${props.comment.user.id}`} className="comment-author-username">{props.comment.user.username}</Link>
                    <div className="comment-date">
                        {new Date(props.comment.created_at).toLocaleDateString()}
                    </div>
                </div>
                <div className="comment-content">{props.comment.content}</div>
            </div>

            {
                store.isAuthenticated && props.comment.user.id == store.user.id &&
                <img
                    className="comment-delete"
                    src="../../../../assets/delete.svg"
                    onClick={handleCommentDelete}
                    alt="Delete commment"
                />
            }
        </div>
    )
});

export default CommentItemList;