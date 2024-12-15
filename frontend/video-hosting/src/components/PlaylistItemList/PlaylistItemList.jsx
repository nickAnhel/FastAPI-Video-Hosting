import { useState, forwardRef, useContext } from "react";
import { Link } from "react-router-dom";
import "./PlaylistItemList.css"

import { Context } from "../../main";
import Options from "../Options/Options";


const PlaylistItemList = forwardRef((props, ref) => {
    const { store } = useContext(Context);

    const [firstVideoImgSrc, setFirstVideoImgSrc] = useState(
        props.playlist.videos.length ?
        `${import.meta.env.VITE_STORAGE_URL}VP@${props.playlist.videos[0]?.id}`:
        "../../../../assets/playlist.svg"
    )

    return (
        <Link className="playlist-item-list" ref={ref} to={`/playlists/${props.playlist.id}`}>
            <div className="videos-count">{props.playlist.videos_count} video{props.playlist.videos_count == 1 ? "" : "s"}</div>

            <img
                className="preview"
                src={firstVideoImgSrc}
                onError={() => setFirstVideoImgSrc("../../../../assets/playlist.svg")}
                alt={props.playlist.title}
            />

            <div className="info">
                <div className="title-wrapper">
                    <div className="title">{props.playlist.title}</div>
                    <Options itemId={props.playlist.id} />
                </div>

                <div className="desc">{props.playlist.description}</div>
            </div>

        </Link>
    )
})

export default PlaylistItemList;