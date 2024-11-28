import { useState, useContext, forwardRef } from "react";
import "./ChannelItemList.css"

import { Context } from "../../main";
import { AlertsContext } from "../../App";
import UserService from "../../service/UserService";
import Loader from "../Loader/Loader";


const ChannelItemList = forwardRef((props, ref) => {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const [imgSrc, setImgSrc] = useState(`${import.meta.env.VITE_STORAGE_URL}PPm@${props.channel.id}?${performance.now()}`);

    const [isLoading, setIsLoading] = useState(false);
    const [isSubscribed, setIsSubsctribed] = useState(props.channel.is_subscribed)
    const [subsCount, setSubsCount] = useState(props.channel.subscribers_count);

    const handleSubscribe = async () => {
        setIsLoading(true);

        try {
            await UserService.subscribeToUser(props.channel.id);
            setIsSubsctribed(true);
            setSubsCount((prev) => prev + 1);
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to subscribe to channel",
                time: 2000,
                type: "error"
            })
            return;
        }

        setIsLoading(false);
        alertsContext.addAlert({
            text: "Successfully subscribed to channel",
            time: 2000,
            type: "success"
        })
    }

    const handleUnsubscribe = async () => {
        setIsLoading(true);

        try {
            await UserService.unsubscribFromuser(props.channel.id);
            setIsSubsctribed(false);
            setSubsCount((prev) => prev - 1);
        } catch (e) {
            alertsContext.addAlert({
                text: "Failed to unsubscribe from channel",
                time: 2000,
                type: "error"
            })
            console.log(e);
        }

        setIsLoading(false);
        alertsContext.addAlert({
            text: "Successfully unsubscribed from channel",
            time: 2000,
            type: "success"
        })
    }

    return (
        <div className="channel-item-list" ref={ref}>
            <div className="left">
                <img
                    className="channel-photo"
                    src={imgSrc}
                    onError={() => { setImgSrc("../../../../assets/profile.svg") }}
                    alt={props.channel.username}
                />
                <div className="info">
                    <div className="username">{props.channel.username}</div>
                    <div className="subs">{subsCount.toLocaleString()} subscriber{subsCount == 1 ? "" : "s"}</div>
                </div>
            </div>
            <div className="right">
                {
                    isSubscribed ?
                        <button
                            className="btn unsubscribe"
                            onClick={handleUnsubscribe}
                        >
                            {isLoading ? <Loader /> : "Unsubscribe"}
                        </button>
                        :
                        <button
                            className="btn"
                            onClick={handleSubscribe}
                            disabled={!store.isAuthenticated}
                        >
                            {isLoading ? <Loader /> : "Subscribe"}
                        </button>

                }

            </div>
        </div>
    )
})

export default ChannelItemList;