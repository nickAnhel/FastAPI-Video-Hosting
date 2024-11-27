import { useState, createRef, useRef, useEffect } from "react";
import { useQuery } from "@siberiacancode/reactuse";
import "./ChannelsList.css"

import Loader from "../Loader/Loader";
import ChannelItemList from "../ChannelItemList/ChannelItemList";

const CHANNELS_IN_PORTION = 10;


function ChannelsList({ fetchChannels, filters }) {
    const lastItem = createRef();
    const observerLoader = useRef();

    const [channels, setChannels] = useState([]);
    const [offset, setOffset] = useState(0);

    const { isLoading, isError, isSuccess, error } = useQuery(
        async () => {
            const params = {
                ...filters,
                offset: offset,
                limit: CHANNELS_IN_PORTION,
            }
            const res = await fetchChannels(params);
            return res.data;
        },
        {
            keys: [offset],
            onSuccess: (fetchedChannels) => {
                setChannels((prevChannels) => [...prevChannels, ...fetchedChannels]);
            }

        }
    );

    const actionInSight = (entries) => {
        if (entries[0].isIntersecting && offset < CHANNELS_IN_PORTION * 5) {
            setOffset((prev) => prev + CHANNELS_IN_PORTION);
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
        <div className="channels-list">
            <div className="channels">
                {
                    channels.map((channel, index) => {
                        if (index + 1 == channels.length) {
                            return <ChannelItemList key={channel.id} channel={channel} ref={lastItem} />
                        }
                        return <ChannelItemList key={channel.id} channel={channel} />
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

export default ChannelsList;