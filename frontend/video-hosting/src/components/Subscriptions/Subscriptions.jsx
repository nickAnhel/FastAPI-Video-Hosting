import { useEffect, useState, useContext } from "react";
import "./Subscriptions.css"

import { Context } from "../../main";
import VideoService from "../../service/VideoService";
import UserService from "../../service/UserService";
import Unauthorized from "../Unauthorized/Unauthorized";
import ChannelsRow from "../ChannelsRow/ChannelsRow";
import VideosGrid from "../VideosGrid/VideosGrid";


function Subscriptions() {
    const { store } = useContext(Context);

    if (!store.isAuthenticated) {
        return (
            <div className="subcriptions">
                <Unauthorized />
            </div>
        )
    }

    return (
        <div className="subcriptions">
            <ChannelsRow fetchChannels={UserService.getSubsctiptions} filters={{ user_id: store.user.id }} />
            <VideosGrid fetchVideos={VideoService.getSubscriptions} filters={{order: "created_at", desc: true}}/>
        </div>
    )
}

export default Subscriptions;