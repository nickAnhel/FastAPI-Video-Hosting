import { useState, useContext, useEffect } from "react";
import "./Playlists.css"

import { Context } from "../../main";
import { AlertsContext, OptionsContext, ShareModalContext } from "../../App";
import PlaylistService from "../../service/PlaylistService";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import PlaylistsList from "../../components/PlaylistsList/PlaylistsList";
import Loader from "../../components/Loader/Loader";
import Modal from "../../components/Modal/Modal";


function Playlists() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const optionsContext = useContext(OptionsContext);
    const shareModalContext = useContext(ShareModalContext);

    const [refresh, setRefresh] = useState(false);
    const [isModalActive, setIsModalActive] = useState(false);

    const [isLoading, setIsLoading] = useState(false);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [isPrivate, setIsPrivate] = useState(false);

    const handleShare = (itemId, page) => {
        shareModalContext.setIsActive(true);
        shareModalContext.setLink(`${import.meta.env.VITE_HOST}/${page}/${itemId}`);
    }

    const handleDeletePlaylist = async (itemId) => {
        try {
            await PlaylistService.deletePlylistById(itemId);
            setRefresh((prev) => !prev)
            alertsContext.addAlert({
                text: "Playlist deleted successfully",
                time: 2000,
                type: "success"
            })
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to delete playlist",
                time: 2000,
                type: "error"
            })
        }
    }

    useEffect(() => {
        let options = [
            {
                text: "Share",
                iconSrc: "../../../assets/share.svg",
                actionHandler: handleShare,
                params: "playlists",
            }
        ]

        if (store.isAuthenticated) {
            options = [
                {
                    text: "Delete playlist",
                    iconSrc: "../../../assets/delete.svg",
                    actionHandler: handleDeletePlaylist,
                },
                ...options,
            ]
        }

        optionsContext.setOptions(options)
    }, [store.isAuthenticated])

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
