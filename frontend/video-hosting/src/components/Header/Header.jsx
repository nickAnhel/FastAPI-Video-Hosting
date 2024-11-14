import { useContext } from "react";
import { observer } from "mobx-react-lite";
import { Link } from "react-router-dom";
import "./Header.css"

import { Context } from "../../main";
import Search from "../Search/Search";


function Header() {
    const { store } = useContext(Context);

    return (
        <div className="header">
            <div className="left">
                <Link to="/" className="logo-link">
                    <img src="../../../../assets/logo.svg" alt="Logo" />
                    <div className="logo">ТипоTube</div>
                </Link>
            </div>

            <Search />
            <div className="right">
                {
                    store.isAuthenticated
                        ?
                        <>
                            <img src="../../../../assets/create.svg" alt="Create Video" />
                            <img src="../../../../assets/notifications.svg" alt="Notifications" />
                            <Link to="/me">
                                <img src="../../../../assets/profile.svg" alt="Me" />
                            </Link>
                        </>
                        : <>
                            <Link to="/login">
                                <img src="../../../../assets/login.svg" alt="Login" />
                            </Link>
                        </>

                }
            </div>
        </div>
    );
}

export default observer(Header)