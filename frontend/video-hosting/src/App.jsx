import { useEffect, useContext } from 'react'
import {observer} from "mobx-react-lite";
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import './App.css'

import { Context } from './main'
import Header from './components/Header/Header'
import Login from './components/Login/Login'
import Register from './components/Register/Register';
import Content from './components/Content/Content'
import Me from './components/Me/Me'
import Profile from './components/Profile/Profile';
import Settings from './components/Settings/Settings';
import NotFound from './components/NotFound/NotFound';
import InWork from './components/InWork/InWork';


function Layout() {
    return (
        <>
            <Header />
            <Outlet />
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
                        element: <InWork />
                    },
                    {
                        path: "/trending",
                        element: <InWork />
                    },
                    {
                        path: "/channels",
                        element: <InWork />
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

    useEffect(() => {
        if (localStorage.getItem('token')) {
            store.checkAuth();
        }
    }, [])

    if (store.isLoading) {
        return <div>Loading...</div>
    }

    return (
        <>
            <RouterProvider router={router} />
        </>
    )
}

export default observer(App);
