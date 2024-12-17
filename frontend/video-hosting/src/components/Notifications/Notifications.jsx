import { useState, useRef, useEffect, createRef } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@siberiacancode/reactuse";
import "./Notifications.css"

import NotificationsService from "../../service/NotificationsService";
import Loader from "../Loader/Loader";
import Notification from "../Notification/Notification";


const NOTIFICATIONS_IN_PORTION = 10;


function Notifications() {
    const notificationsRef = useRef(null);
    const [isFirstRender, setIsFirstRender] = useState(true);

    const lastItem = createRef();
    const observerLoader = useRef();

    const [isOpen, setIsOpen] = useState(false);
    const [refresh, setRefresh] = useState(false);

    const [notificationsCount, setNotificationsCount] = useState(0);
    const [notifications, setNotifications] = useState([]);
    const [offset, setOffset] = useState(0);


    useEffect(() => {
        const getNotificationsCount = async () => {
            const res = await NotificationsService.getNewNotificationsCount();
            setNotificationsCount(res.data);
        }

        getNotificationsCount();
        const timer = setInterval(getNotificationsCount, 60000);

        return () => {
            clearInterval(timer);
        }
    }, [])

    useEffect(() => {
        setIsFirstRender(true);
    }, [])

    useEffect(() => {
        const fetchData = async () => {
            setOffset(0);
            setNotifications([]);
            await getNotificationsCount();
        }
        fetchData();
    }, [refresh])

    useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpen]);

    const { isLoading, isError, isSuccess, error } = useQuery(
        async () => {
            const params = {
                offset: offset,
                limit: NOTIFICATIONS_IN_PORTION,
            }

            const res = await NotificationsService.getNotifications(params);
            return res.data;
        },
        {
            enabled: !isFirstRender,
            keys: [offset, refresh],
            onSuccess: (fetchedNotifications) => {
                setNotifications((prevNotifications) => [...prevNotifications, ...fetchedNotifications]);
            },
        },
    );

    const actionInSight = (entries) => {
        if (entries[0].isIntersecting && offset < NOTIFICATIONS_IN_PORTION * 5) {
            setOffset((prev) => prev + NOTIFICATIONS_IN_PORTION);
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

    const handleToggleNotifications = (event) => {
        event.stopPropagation();
        event.preventDefault();
        setIsOpen(!isOpen);
        setIsFirstRender(false);
        setNotificationsCount(0);
    }

    const handleClickOutside = (event) => {
        if (notificationsRef.current && !notificationsRef.current.contains(event.target)) {
            setIsOpen(false);
        }
    };

    const refreshList = () => {
        setRefresh(!refresh);
    }

    const getNumberRepresentation = (cnt) => {
        if (cnt < 100) {
            return cnt
        } else if (cnt < 1000) {
            return "99+"
        } else if (cnt < 10000) {
            return Math.floor(cnt / 1000) + "k"
        } else if (cnt < 100000) {
            return Math.floor(cnt / 1000) + "k"
        } else {
            return "∞"
        }
    }

    return (
        <div className="notifications" ref={notificationsRef}>
            <div className="notifications-btn">
                <img
                    className="notifications-img"
                    src="../../../../assets/notifications.svg"
                    alt="Notifications"
                    onClick={handleToggleNotifications}
                />

                {
                    notificationsCount != 0 &&
                    <div className="notifications-count">{getNumberRepresentation(notificationsCount)}</div>
                }
            </div>

            <div
                className={isOpen ? "notifications-menu active" : "notifications-menu"}
            >
                <div className="notifications-header">
                    <h3>Notifications</h3>
                    <Link
                        to={"/me/settings"}
                        onClick={() => setIsOpen(false)}
                    >
                        <img
                            className="settings-link-img"
                            src="../../../../assets/settings.svg"
                            alt="Notifications Settings"
                        />
                    </Link>
                </div>

                <div className="notifications-list">
                    {
                        isSuccess && notifications.map((notification, index) => {
                            if (index + 1 == notifications.length) {
                                return <Notification key={index} notification={notification} setOpen={setIsOpen} refresh={refreshList} ref={lastItem} />
                            }
                            return <Notification key={index} notification={notification} setOpen={setIsOpen} refresh={refreshList} />
                        })
                    }
                    {
                        (!isLoading && notifications.length == 0) ? <div className="hint">No notifications yet</div> : ""
                    }
                    {
                        isLoading &&
                        <div className="loader"><Loader /></div>
                    }
                </div>
            </div>
        </div>
    )
}

export default Notifications;