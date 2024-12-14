import { useEffect, useContext, createContext } from 'react'
import { createBrowserRouter, RouterProvider, Outlet, useParams } from "react-router-dom";
import { observer } from "mobx-react-lite";
import './App.css'

import { Context } from './main'
import useAlerts from './hooks/useAlerts';

import Header from './components/Header/Header'
import Login from './components/Login/Login'
import Register from './components/Register/Register';
import Content from './components/Content/Content'
import Me from './components/Me/Me'
import Profile from './components/Profile/Profile';
import Settings from './components/Settings/Settings';
import NotFound from './components/NotFound/NotFound';
import InWork from './components/InWork/InWork';
import Loader from "./components/Loader/Loader";
import Alerts from './components/Alerts/Alerts';
import VideoDetails from './components/VideoDetails/VideoDetails';
import Subscriptions from './components/Subscriptions/Subscriptions';
import ChannelDetails from './components/ChannelDetails/ChannelDetails';
import CreateVideo from './components/CreateVideo/CreateVideo';
import PlaylistDetails from './components/PlaylistDetails/PlaylistDetails';

import Main from './pages/Main/Main';
import Trending from './pages/Trending/Trending';
import Channels from './pages/Channels/Channels';
import History from './pages/History/History';
import Liked from './pages/LIked/Liked';
import SubscriptionsList from './pages/SubscriptionsList/SubscriptionsList';
import Playlists from './pages/Playlists/Playlists';


export const AlertsContext = createContext(null);


function Layout() {
    const alertsContext = useContext(AlertsContext);

    return (
        <>
            <Header />
            <Outlet />
            <Alerts alerts={alertsContext.alerts} />
        </>
    )
}


const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout />,
        errorElement: <NotFound />,
        children: [
            {
                path: "/",
                element: <Content />,
                children: [
                    {
                        path: "/",
                        element: <Main />
                    },
                    {
                        path: "/trending",
                        element: <Trending />
                    },
                    {
                        path: "/channels",
                        element: <Channels />
                    },
                    {
                        path: "/subscriptions",
                        element: <Outlet />,
                        children: [
                            {
                                path: "/subscriptions/",
                                element: <Subscriptions />
                            },
                            {
                                path: "/subscriptions/list",
                                element: <SubscriptionsList />
                            }
                        ]
                    },
                    {
                        path: "/history",
                        element: <History />
                    },
                    {
                        path: "/playlists",
                        element: <Playlists />
                    },
                    {
                        path: "/liked-videos",
                        element: <Liked />
                    },
                ]
            },
            {
                path: "/login",
                element: <Login />,
            },
            {
                path: "/register",
                element: <Register />,
            },
            {
                path: "/me",
                element: <Me />,
                children: [
                    {
                        path: "/me/profile",
                        element: <Profile />,
                    },
                    {
                        path: "/me/settings",
                        element: <Settings />,
                    },
                ]
            },
            {
                path: "/create",
                element: <CreateVideo />,
            },
            {
                path: "/videos/:id",
                element: <VideoDetails />,
            },
            {
                path: "/channels/:id",
                element: <ChannelDetails />,
            },
            {
                path: "/playlists/:id",
                element: <PlaylistDetails />,
            },
        ]
    }
])


function App() {
    const { store } = useContext(Context)

    const { alerts, addAlert, removeAlert } = useAlerts();

    useEffect(() => {
        if (localStorage.getItem('token')) {
            store.checkAuth();
        }
    }, [])

    if (store.isLoading) {
        return <Loader />
    }
    return (
        <AlertsContext.Provider value={{ alerts, addAlert, removeAlert }}>
            <RouterProvider router={router} />
        </AlertsContext.Provider>
    )
}

export default observer(App);
