import { useState, useContext } from "react";
import "./Playlists.css"

import { Context } from "../../main";
import { AlertsContext } from "../../App";
import PlaylistService from "../../service/PlaylistService";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import PlaylistsList from "../../components/PlaylistsList/PlaylistsList";
import Loader from "../../components/Loader/Loader";
import Modal from "../../components/Modal/Model";


function Playlists() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);

    const [refresh, setRefresh] = useState(false);
    const [isModalActive, setIsModalActive] = useState(false);

    const [isLoading, setIsLoading] = useState(false);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [isPrivate, setIsPrivate] = useState(false);

    const handleCreate = async () => {
        setIsLoading(true);

        try {
            const data = {
                title: title,
                description: description,
                private: isPrivate,
            }
            await PlaylistService.createPlaylist(data);
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to create playlist",
                time: 2000,
                type: "error"
            })
        }

        setIsLoading(false);
        setIsModalActive(false);
        setRefresh((prev) => !prev)
    }

    const handleClear = () => {
        setTitle("");
        setDescription("");
        setIsPrivate(false);
    }

    if (!store.isAuthenticated) {
        return (
            <div className="playlists-page">
                <Unauthorized />
            </div>
        )
    }

    return (
        <div className="playlists-page">
            <PlaylistsList filters={{ owner_id: store.user.id }} refresh={refresh} />
            <button
                className="create-playlist-btn"
                onClick={(e) => setIsModalActive(true)}
            >
                Create playlist
            </button>

            <Modal active={isModalActive} setActive={setIsModalActive}>
                <h1>Create Playlist</h1>
                <div className="create-playlist">
                    <input
                        className="playlist-title"
                        type="text"
                        value={title}
                        maxLength={50}
                        placeholder="Title"
                        onChange={(e) => setTitle(e.target.value)}
                        style={{ borderColor: title.trim() ? "#fff" : "#7e7e7e" }}
                    />

                    <div
                        className="playlist-desc-wrapper"
                        style={{ borderColor: description.trim() ? "#fff" : "#7e7e7e" }}
                    >
                        <textarea
                            className="playlist-desc"
                            value={description}
                            maxLength={255}
                            placeholder="Description"
                            onChange={(e) => setDescription(e.target.value)}
                        ></textarea>
                        <span className="playlist-desc-length">{description.trim().length} / 255</span>
                    </div>

                    <div className="playlist-private">
                        <input
                            id="isPrivate"
                            type="checkbox"
                            checked={isPrivate}
                            onChange={e => setIsPrivate(e.target.checked)}
                        />
                        <label htmlFor="isPrivate">Private</label>
                    </div>

                    <button
                        className="create"
                        onClick={handleCreate}
                        disabled={!title.trim() || !description.trim()}
                    >
                        {isLoading ? <Loader /> : "Create"}
                    </button>

                    <button
                        className="clear"
                        onClick={handleClear}
                    >
                        Clear
                    </button>
                </div>

            </Modal>
        </div>
    )
}

export default Playlists;
