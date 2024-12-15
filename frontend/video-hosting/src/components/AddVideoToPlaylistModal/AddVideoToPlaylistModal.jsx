import { useState, useContext, useEffect } from "react";
import "./AddVideoToPlaylistModal.css"

import { AddVideoModalContext, AlertsContext } from "../../App";
import PlaylistService from "../../service/PlaylistService";
import Modal from "../Modal/Modal";


function AddVideoToPlaylistModal() {
    const alertsContext = useContext(AlertsContext);
    const addVideoContext = useContext(AddVideoModalContext);
    const [update, setUpdate] = useState(1);
    const [playlists, setPlaylists] = useState([])

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await PlaylistService.getUserPlaylistExcludeVideo(addVideoContext.videoId);
                setPlaylists(res.data);
            } catch (e) {
                console.log(e);
            }
        }
        fetchData();
    }, [addVideoContext.videoId, addVideoContext.active, update])

    const handleAddToPlaylist = async (playlistId) => {
        try {
            await PlaylistService.addVideoToPlaylist(addVideoContext.videoId, playlistId);
            setUpdate(update + 1);
            alertsContext.addAlert({
                text: "Successfully added video to playlist",
                time: 2000,
                type: "success"
            })
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to add video to playlist",
                time: 2000,
                type: "error"
            })
        }
    }

    return (
        <Modal
            active={addVideoContext.active}
            setActive={addVideoContext.setActive}
        >
            <div
                className="playlists-to-add"
            >
                {
                    playlists.length == 0 ?
                        "No playlists to add this video" : <>
                            <h2>Click on playlist to add video</h2>
                            <div className="playlist-items">
                                {
                                    playlists.map((playlist, index) => {
                                        return (
                                            <div
                                                key={index}
                                                className="playlist-item"
                                                onClick={(e) => handleAddToPlaylist(playlist.id)}
                                            >
                                                {playlist.title}
                                            </div>
                                        )
                                    })
                                }
                            </div>
                        </>
                }


            </div>
        </Modal>
    )
}

export default AddVideoToPlaylistModal;