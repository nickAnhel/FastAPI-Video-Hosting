import { useContext } from "react";
import "./SubscriptionsList.css"

import { Context } from "../../main";
import UserService from "../../service/UserService";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import ChannelsList from "../../components/ChannelsList/ChannelsList";


function SubscriptionsList() {
    const { store } = useContext(Context);

    if (!store.isAuthenticated) {
        return <Unauthorized />
    }

    return (
        <div className="subscriptions-list-page">
            <ChannelsList fetchChannels={UserService.getSubsctiptions} filters={{user_id: store.user.id}} />
        </div>
    )
}

export default SubscriptionsList;