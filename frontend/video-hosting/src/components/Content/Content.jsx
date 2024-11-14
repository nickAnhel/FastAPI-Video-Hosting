import { Outlet } from "react-router-dom"
import "./Content.css"

import Sidebar from "../Sidebar/Sidebar"


function Content() {
    return (
        <div className="main">
            <Sidebar />
            <Outlet />
        </div>
    )
}

export default Content