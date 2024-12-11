import { useState, useContext, createRef, useRef, useEffect } from "react";
import { useQuery } from "@siberiacancode/reactuse";
import "./CommentsList.css"

import { Context } from "../../main";
import CommentService from "../../service/CommentService";
import Loader from "../Loader/Loader";
import CommentItemList from "../CommentItemList/CommentsItemList";


const COMMENTS_IN_PORTION = 10;


function CommentsList({ videoId }) {
    const { store } = useContext(Context);

    const lastItem = createRef();
    const observerLoader = useRef();

    const [commentContent, setCommentContent] = useState("");
    const [isLoadingComment, setIsLoadingComment] = useState(false);

    const [comments, setComments] = useState([]);
    const [offset, setOffset] = useState(0);

    const { isLoading, isError, isSuccess, error } = useQuery(
        async () => {
            const params = {
                video_id: videoId,
                order: "created_at",
                desc: true,
                offset: offset,
                limit: COMMENTS_IN_PORTION,
            }
            const res = await CommentService.getComments(params);
            return res.data;
        },
        {
            keys: [offset],
            onSuccess: (fetchedComments) => {
                setComments((prevComments) => [...prevComments, ...fetchedComments]);
            }

        }
    );

    const actionInSight = (entries) => {
        if (entries[0].isIntersecting && offset < COMMENTS_IN_PORTION * 5) {
            setOffset((prev) => prev + COMMENTS_IN_PORTION);
        }
    };

    useEffect(() => {
        if (observerLoader.current) {
            observerLoader.current.disconnect();
        }

        observerLoader.current = new IntersectionObserver(actionInSight);

        if (lastItem.current) {
            observerLoader.current.observe(lastItem.current);
        }
    }, [lastItem]);

    const handleLeaveComment = async () => {
        setIsLoadingComment(true);
        try {
            if (commentContent.trim().length != 0) {
                const res = await CommentService.createComment(videoId, commentContent.trim());
                console.log(res.data)
                setComments((prevComments) => [res.data, ...prevComments]);
            }
        } catch (e) {
            console.log(e);
        }
        setIsLoadingComment(false);
        setCommentContent("");
    }

    const removeCommentFromList = (commentId) => {
        setComments((prevComments) => prevComments.filter((comment, _) => comment.id != commentId));
    }

    if (isError) {
        console.log(error);
        return;
    }

    return (
        <div className="comments-list">
            {
                store.isAuthenticated &&

                <div className="comment-create">
                    <div className="comment-input-wrapper">
                        <textarea
                            className="comment-input"
                            placeholder="Leave a comment..."
                            value={commentContent}
                            onChange={(e) => setCommentContent(e.target.value)}
                            maxLength={255}
                        ></textarea>
                        <span className="comment-length">{commentContent.trim().length} / 255</span>
                    </div>
                    <button
                        className="comment-create-btn"
                        disabled={commentContent.trim().length == 0}
                        onClick={handleLeaveComment}
                    >
                        {
                            isLoadingComment ?
                            <Loader />
                            :
                            <img
                                src="../../../../assets/send.svg"
                                alt="Leave comment"
                            />
                        }
                    </button>
                </div>
            }

            <div className="comments">
                {
                    comments.length == 0 && "No comments"
                }
                {
                    comments.map((comment, index) => {
                        if (index + 1 == comments.length) {
                            return <CommentItemList key={comment.id} comment={comment} ref={lastItem} removeComment={removeCommentFromList} />
                        }
                        return <CommentItemList key={comment.id} comment={comment} removeComment={removeCommentFromList} />
                    })
                }
            </div>

            {
                isLoading &&
                <div className="loader"><Loader /></div>
            }
        </div>
    )
}

export default CommentsList;