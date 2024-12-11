import { useState, createRef, useRef, useEffect } from "react";
import { useQuery } from "@siberiacancode/reactuse";
import "./VideosList.css"

import VideoItemList from "../VideoItemList/VideoItemList";
import Loader from "../Loader/Loader";


const VIDEOS_IN_PORTION = 9;


function VideosList({ fetchVideos, filters, clear }) {
    const lastItem = createRef();
    const observerLoader = useRef();

    const [videos, setVideos] = useState([]);
    const [offset, setOffset] = useState(0);

    useEffect(() => {
        setVideos([]);
    }, [clear])

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
            keys: [offset],
            onSuccess: (fetchedVideos) => {
                setVideos((prevVideos) => [...prevVideos, ...fetchedVideos]);
            }

        }
    );

    const actionInSight = (entries) => {
        if (entries[0].isIntersecting && offset < VIDEOS_IN_PORTION * 5) {
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
        <div className="videos-list">
            <div className="videos">
                {
                    videos.map((video, index) => {
                        if (index + 1 == videos.length) {
                            return <VideoItemList key={video.id} video={video} ref={lastItem}/>
                        }
                        return <VideoItemList key={video.id} video={video} />
                    })
                }
                {
                    (!isLoading && videos.length == 0) ? <div className="hint">No videos</div> : ""
                }
            </div>

            {
                isLoading &&
                <div className="loader"><Loader /></div>
            }
        </div>
    )
}

export default VideosList;