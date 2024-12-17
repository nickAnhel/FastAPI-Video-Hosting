import { useState, createRef, useRef, useEffect } from "react";
import { useQuery } from "@siberiacancode/reactuse";
import "./VideosGrid.css"

import VideoItemGrid from "../VideoItemGrid/VideoItemGrid";
import Loader from "../Loader/Loader";


const VIDEOS_IN_PORTION = 5;


function VideosGrid({ fetchVideos, filters, refresh }) {
    const lastItem = createRef();
    const observerLoader = useRef();

    const [videos, setVideos] = useState([]);
    const [offset, setOffset] = useState(0);

    useEffect(() => {
        setVideos([]);
        setOffset(0);
    }, [refresh])

    const { isLoading, isError, isSuccess, error } = useQuery(
        async () => {
            const params = {
                ...filters,
                offset: offset,
                limit: VIDEOS_IN_PORTION,
            }
            const res = await fetchVideos(params);
            return res.data;
        },
        {
            keys: [offset, refresh],
            onSuccess: (fetchedVideos) => {
                setVideos((prevVideos) => [...prevVideos, ...fetchedVideos]);
            }

        }
    );

    const actionInSight = (entries) => {
        if (entries[0].isIntersecting && offset < VIDEOS_IN_PORTION * 10) {
            setOffset((prev) => prev + VIDEOS_IN_PORTION);
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
        <div className="videos-grid">
            <div className="videos">
                {
                    videos.map((video, index) => {
                        if (index + 1 == videos.length) {
                            return <VideoItemGrid key={video.id} video={video} ref={lastItem} />
                        }
                        return <VideoItemGrid key={video.id} video={video} />
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

export default VideosGrid;