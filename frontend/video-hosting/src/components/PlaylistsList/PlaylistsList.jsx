import { useState, createRef, useRef, useEffect } from "react";
import { useQuery } from "@siberiacancode/reactuse";
import "./PlaylistsList.css"

import PlaylistService from "../../service/PlaylistService";
import Loader from "../Loader/Loader";
import PlaylistItemList from "../PlaylistItemList/PlaylistItemList";


const PLAYLISTS_IN_PORTION = 9;


function PlaylistsList({ filters, refresh }) {
    const lastItem = createRef();
    const observerLoader = useRef();

    const [playlists, setPlaylists] = useState([]);
    const [offset, setOffset] = useState(0);

    useEffect(() => {
        setPlaylists([]);
    }, [refresh])

    const { isLoading, isError, isSuccess, error } = useQuery(
        async () => {
            const params = {
                ...filters,
                offset: offset,
                limit: PLAYLISTS_IN_PORTION,
            }
            const res = await PlaylistService.getPlaylists(params);
            return res.data;
        },
        {
            keys: [offset, refresh],
            onSuccess: (fetchedPlaylists) => {
                setPlaylists((prevPlaylists) => [...prevPlaylists, ...fetchedPlaylists]);
            }

        }
    );

    const actionInSight = (entries) => {
        if (entries[0].isIntersecting && offset < PLAYLISTS_IN_PORTION * 5) {
            setOffset((prev) => prev + PLAYLISTS_IN_PORTION);
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

    if (isError) {
        console.log(error);
        return;
    }

    return (
        <div className="playlists-list">
            <div className="playlists">
                {
                    playlists.map((playlist, index) => {
                        if (index + 1 == playlist.length) {
                            return <PlaylistItemList key={playlist.id} playlist={playlist} ref={lastItem}/>
                        }
                        return <PlaylistItemList key={playlist.id} playlist={playlist} />
                    })

                }
                {
                    (!isLoading && playlists.length == 0) ? <div className="hint">No playlists</div> : ""
                }
            </div>

            {
                isLoading &&
                <div className="loader"><Loader /></div>
            }
        </div>
    )
}

export default PlaylistsList;
