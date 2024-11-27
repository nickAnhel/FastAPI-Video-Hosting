import { useEffect, useContext, createContext } from 'react'
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
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

import Main from './pages/Main/Main';
import Trending from './pages/Trending/Trending';
import Channels from './pages/Channels/Channels';


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
                        path: "/channels",
                        element: <InWork />
                    },
                    {
                        path: "/subscriptions",
                        element: <InWork />
                    },
                    {
                        path: "/history",
                        element: <InWork />
                    },
                    {
                        path: "/playlists",
                        element: <InWork />
                    },
                    {
                        path: "/watch-later",
                        element: <InWork />
                    },
                    {
                        path: "/liked-videos",
                        element: <InWork />
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
