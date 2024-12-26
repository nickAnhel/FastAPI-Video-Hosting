import { useState, useEffect, useContext } from "react";
import { observer } from "mobx-react-lite";
import { Link } from "react-router-dom";
import "./Header.css"

import { Context } from "../../main";
import Search from "../Search/Search";
import Notifications from "../Notifications/Notifications";


function Header() {
    const { store } = useContext(Context);

    const [imgSrc, setImgSrc] = useState();

    useEffect(() => {
        setImgSrc(`${import.meta.env.VITE_STORAGE_URL}PPs@${store.user.id}?${performance.now()}`);
    }, [store.user?.id, store.isChangedProfilePhoto])

    return (
        <div className="header">
            <div className="left">
                <Link to="/" className="logo-link">
                    <img src="../../../../assets/logo.png" alt="Logo" />
                    {/* <div className="logo">ТипоTube</div> */}
                </Link>
            </div>

            <Search />
            <div className="right">
                {
                    store.isAuthenticated
                        ?
                        <>
                            <Link to="/create">
                                <img src="../../../../assets/create.svg" alt="Create Video" />
                            </Link>

                            <Notifications />

                            <Link to="/me/profile">
                                <img
                                    // src="../../../../assets/profile.svg" alt="Me"
                                    src={imgSrc}
                                    onError={() => { setImgSrc("../../../../assets/profile.svg") }}
                                    alt="Profile Picture"
                                />
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