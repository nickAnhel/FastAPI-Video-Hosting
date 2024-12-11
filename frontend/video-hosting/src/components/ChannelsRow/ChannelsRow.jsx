import { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import "./ChannelsRow.css"

import { Context } from "../../main";
import ChannelItemRow from "../ChannelItemRow/ChannelItemRow";


function ChannelsRow({ fetchChannels, filters }) {
    const { store } = useContext(Context);

    const [channels, setChannels] = useState([]);

    useEffect(() => {
        const wrapper = async () => {
            try {
                const res = await fetchChannels(filters);
                setChannels(res.data);
            } catch (e) {
                console.log(e);
            }
        }
        wrapper();
    }, [store.user.id])

    return (
        <div className="channels-row">
            <div className="channels">
                {
                    channels.length != 0 ?
                    channels.map((channel, index) => {
                        return (
                            <ChannelItemRow key={channel.id} channel={channel} />
                        )
                    })
                    :
                    <p>
                        No subscriptions yet
                    </p>
                }
            </div>

            {
                channels.length != 0 &&
                <Link className="all" to={"/subscriptions/list"}>
                    All
                </Link>
            }
        </div>
    )
}

export default ChannelsRow;