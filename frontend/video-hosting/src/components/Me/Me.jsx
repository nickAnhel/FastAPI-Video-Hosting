import { useContext } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { observer } from "mobx-react-lite";
import "./Me.css"

import Unauthorized from "../Unauthorized/Unauthorized";
import { Context } from "../../main";

function Me() {
    const { store } = useContext(Context);

    if (!store.isAuthenticated) {
        return <Unauthorized />
    }

    return (
        <div className="me">
            <div className="pages">
                <NavLink
                    to="/me/profile"
                    className={({ isActive }) => isActive ? "page active" : "page"}
                >
                    Profile
                </NavLink>
                <NavLink
                    to="/me/settings"
                    className={({ isActive }) => isActive ? "page active" : "page"}
                >
                    Settings
                </NavLink>
            </div>
            <div className="page-content">
                <Outlet></Outlet>
            </div>
        </div>
    )
}

export default observer(Me);