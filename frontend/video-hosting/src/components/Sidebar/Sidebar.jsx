import { NavLink } from "react-router-dom"
import "./Sidebar.css"


function Sidebar() {
    return (
        <div className="sidebar">
            <NavLink to="/" className={({ isActive }) => isActive ? "item active" : "item"}>
                <img src="../../../../assets/home.svg" alt="Main" />
                <div>Main</div>
            </NavLink>

            <NavLink to="/trending" className="item">
                <img src="../../../../assets/trending.svg" alt="Main" />
                <div>Trending</div>
            </NavLink>
            <NavLink to="/channels" className="item">
                <img src="../../../../assets/channels.svg" alt="Main" />
                <div>Channels</div>
            </NavLink>

            <hr />

            <NavLink to="/subscriptions" className="item">
                <img src="../../../../assets/subscriptions.svg" alt="Main" />
                <div>Subscriptions</div>
            </NavLink>

            <hr />

            <NavLink to="/history" className="item">
                <img src="../../../../assets/history.svg" alt="Main" />
                <div>History</div>
            </NavLink>
            <NavLink to="/playlists" className="item">
                <img src="../../../../assets/playlists.svg" alt="Main" />
                <div>Playlists</div>
            </NavLink>
            <NavLink to="/watch-later" className="item">
                <img src="../../../../assets/watch-later.svg" alt="Main" />
                <div>Watch Later</div>
            </NavLink>
            <NavLink to="/liked-videos" className="item">
                <img src="../../../../assets/liked-videos.svg" alt="Main" />
                <div>Liked Videos</div>
            </NavLink>
        </div>
    )
}

export default Sidebar