import "./Channels.css"

import UserService from "../../service/UserService";
import ChannelsList from "../../components/ChannelsList/ChannelsList";


function Channels() {
    return (
        <div className="channels-page">
            <ChannelsList
                fetchChannels={UserService.getUsers}
                filters={{
                    order: "subscribers_count",
                    desc: true,
                }}
            />
        </div>
    )
}

export default Channels;