import { useState, useEffect, useContext } from "react";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import "./Profile.css"

import UserService from "../../service/UserService";
import { Context } from "../../main";


function Profile() {
    const { store } = useContext(Context);
    const navigate = useNavigate();

    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingDelete, setIsLoadingDelete] = useState(false);
    const [username, setUsername] = useState("");
    const [about, setAbout] = useState("");
    const [socialLinks, setSocialLinks] = useState([]);

    useEffect(() => {
        setUsername(store.user.username);
        setAbout(store.user.about);
        setSocialLinks(store.user.social_links);
    }, [store.user.social_links]);

    const handleLinkChange = (index, event) => {
        const newLinks = [...socialLinks];
        newLinks[index] = event.target.value;
        setSocialLinks(newLinks);
    };

    const addLink = () => {
        if (socialLinks.length < 10) {
            setSocialLinks([...socialLinks, '']);
        }
    };

    const removeLink = (index) => {
        const newLinks = socialLinks.filter((_, i) => i !== index);
        setSocialLinks(newLinks);
    };

    const handleReset = () => {
        setUsername(store.user.username);
        setAbout(store.user.about);
        setSocialLinks(store.user.social_links);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const data = {
                username: username.trim(),
                about: about.trim(),
                social_links: socialLinks
            };

            const res = await UserService.updateMe(data);
            store.setUser(res.data);
        } catch (error) {
            console.log(error);
        }
        setIsLoading(false);
    };

    const handleLogout = () => {
        store.logout();
        navigate("/login");
    }

    const handleDelete = async () => {
        setIsLoadingDelete(true);
        try {
            await UserService.deleteMe();
            store.logout();
            navigate("/login");
        } catch (error) {
            console.log(error);
        }
        setIsLoadingDelete(false);
    }

    return (
        <div className="profile">
            <form
                className="profile-form"
                onSubmit={(e) => handleSubmit(e)}
            >
                <div>
                    <div className="credentials-wrapper">
                        <img src="../../../../assets/profile.svg" alt="Profile Picture" />
                        <div className="credentials">
                            <input
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                maxLength={50}
                                required
                            />
                            <p className="email">{store.user.email}</p>
                        </div>
                    </div>
                </div>

                <div>
                    <h2>About</h2>
                    <div className="about-wrapper">
                        <textarea
                            className="about"
                            placeholder="About"
                            value={about}
                            onChange={(e) => setAbout(e.target.value)}
                            maxLength={255}
                        ></textarea>
                        <span className="about-length">{about.trim().length} / 255</span>
                    </div>
                </div>

                <div>
                    <h2>Social links</h2>
                    <div className="links">
                        {
                            socialLinks.map((link, index) => (
                                <div key={index} className="link">
                                    <input
                                        type="url"
                                        value={link}
                                        onChange={(event) => handleLinkChange(index, event)}
                                        placeholder={`Link ${index + 1}`}
                                        required
                                    />
                                    <img
                                        onClick={() => removeLink(index)}
                                        src="../../../../assets/delete.svg"
                                        alt={`Delete link ${index + 1}`}
                                    />
                                </div>
                            ))
                        }
                        <button
                            type="button"
                            className="add-link"
                            onClick={(e) => { e.preventDefault(); addLink() }}
                            disabled={socialLinks.length >= 10}
                        >
                            <img src="../../../../assets/add.svg" alt="" />
                        </button>
                    </div>
                </div>

                <div>
                    <h2>Actions</h2>
                    <div className="actions">
                        <button
                            type="button"
                            className="btn logout"
                            onClick={handleLogout}
                        >
                            Log Out
                        </button>
                        <button
                            type="button"
                            className="btn delete"
                            onClick={handleDelete}
                            disabled={isLoadingDelete}
                        >
                            { isLoadingDelete ? "Deleting..." : "Delete Account"}
                        </button>
                    </div>
                </div>

                <button
                    type="submit"
                    className="save-button"
                    disabled={isLoading}
                >
                    { isLoading ? "Saving..." : "Save"}
                </button>
                <button
                    type="submit"
                    className="reset"
                    onClick={handleReset}
                >
                    Reset
                </button>
            </form>
        </div>
    )
}


export default observer(Profile)
