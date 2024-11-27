import ChannelsList from "../../components/ChannelsList/ChannelsList";


import UserService from "../../service/UserService";


function Channels() {
    return (
        <ChannelsList
            fetchChannels={UserService.getUsers}
            filters={{
                order: "subscribers_count",
                desc: true,
            }}
        />
    )
}

export default Channels;