import { useState, useEffect, useContext } from "react";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import "./Profile.css"

import Modal from "../Modal/Model";
import Loader from "../Loader/Loader";
import UserService from "../../service/UserService";
import { Context } from "../../main";
import { AlertsContext } from "../../App";


function Profile() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const navigate = useNavigate();

    const [isLoadingSave, setIsLoadingSave] = useState(false);
    const [isLoadingDelete, setIsLoadingDelete] = useState(false);
    const [isLoadingProfilePhotoUpdate, setIsLoadingProfilePhotoUpdate] = useState(false);
    const [isLoadingProfilePhotoDelete, setIsLoadingProfilePhotoDelete] = useState(false);
    const [imgSrc, setImgSrc] = useState(`${import.meta.env.VITE_STORAGE_URL}PP@${store.user.id}?${performance.now()}`);
    const [isModalActive, setIsModalActive] = useState(false);

    const [username, setUsername] = useState("");
    const [about, setAbout] = useState("");
    const [socialLinks, setSocialLinks] = useState([]);

    const [profilePhoto, setProfilePhoto] = useState(null);
    const [selectedFile, setSelectedFile] = useState();
    const [preview, setPreview] = useState();

    useEffect(() => {
        if (!selectedFile) {
            setPreview(undefined)
            return
        }

        const objectUrl = URL.createObjectURL(selectedFile)
        setPreview(objectUrl)

        return () => URL.revokeObjectURL(objectUrl)
    }, [selectedFile])

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

        setIsLoadingSave(true);
        try {
            const data = {
                username: username.trim(),
                about: about.trim(),
                social_links: socialLinks
            };

            const res = await UserService.updateMe(data);
            store.setUser(res.data);

            alertsContext.addAlert({
                text: "Profile data updated successfully",
                time: 2000,
                type: "success"
            })

        } catch (e) {
            alertsContext.addAlert({
                text: e.response?.data?.detail,
                time: 2000,
                type: "error"
            })

            console.log(e.response?.data?.detail);
        }
        setIsLoadingSave(false);
    };

    const handleLogout = () => {
        store.logout();
        navigate("/login");

        alertsContext.addAlert({
            text: "You have successfully logged out",
            time: 2000,
            type: "success"
        })
    }

    const handleDelete = async () => {
        setIsLoadingDelete(true);

        try {
            await UserService.deleteMe();
            store.logout();
            navigate("/login");
        } catch (e) {
            alertsContext.addAlert({
                text: e.response?.data?.detail,
                time: 2000,
                type: "error"
            })

            console.log(e.response?.data?.detail);
        }

        setIsLoadingDelete(false);

        alertsContext.addAlert({
            text: "Your account successfully deleted",
            time: 2000,
            type: "success"
        })
    }

    const handleProfilePhotoUpdate = async () => {
        setIsLoadingProfilePhotoUpdate(true);

        try {
            const formData = new FormData()
            formData.append("photo", profilePhoto);
            await UserService.updateProfilePhoto(formData);
            setImgSrc(`${import.meta.env.VITE_STORAGE_URL}PP@${store.user.id}?${performance.now()}`);

            alertsContext.addAlert({
                text: "Profile photo updated successfully",
                time: 2000,
                type: "success"
            })
        } catch (e) {
            console.log(e.response?.data?.detail);
        }

        setIsLoadingProfilePhotoUpdate(false);
        setIsModalActive(false);
    }

    const handleProfilePhotoDelete = async () => {
        setIsLoadingProfilePhotoDelete(true);

        try {
            await UserService.deleteProfilePhoto();

            alertsContext.addAlert({
                text: "Profile deleted successfully",
                time: 2000,
                type: "success"
            })
        } catch (e) {
            console.log(e.response?.data?.detail);
        }

        setImgSrc("../../../../assets/profile.svg");
        setIsLoadingProfilePhotoDelete(false);
        setIsModalActive(false);
    }

    const handleSelectFile = e => {
        if (!e.target.files || e.target.files.length === 0) {
            setSelectedFile(undefined)
            return
        }

        setSelectedFile(e.target.files[0])
    }


    return (
        <div className="profile">
            <form
                className="profile-form"
                onSubmit={(e) => handleSubmit(e)}
            >
                <div>
                    <div className="credentials-wrapper">
                        <img
                            src={imgSrc}
                            onError={() => { setImgSrc("../../../../assets/profile.svg") }}
                            alt="Profile Picture"
                            onClick={() => { setIsModalActive(true) }}
                        />

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
                            {isLoadingDelete ? <Loader /> : "Delete Account"}
                        </button>
                    </div>
                </div>

                <button
                    type="submit"
                    className="save-button"
                    disabled={isLoadingSave}
                >
                    {isLoadingSave ? <Loader /> : "Save"}
                </button>
                <button
                    type="reset"
                    className="reset"
                    onClick={handleReset}
                >
                    Reset
                </button>
            </form>

            <Modal active={isModalActive} setActive={setIsModalActive}>
                <form className="image-form">
                    <label htmlFor="profile-photo-file">
                        <img
                            src={preview}
                            alt="🖫"
                        />
                        <input
                            type="file"
                            id="profile-photo-file"
                            accept=".png, .jpg, .jpeg"
                            onChange={e => {setProfilePhoto(e.target.files[0]); handleSelectFile(e)}}
                        />
                    </label>
                    <button
                        className="btn"
                        type="submit"
                        onClick={e => { e.preventDefault(); handleProfilePhotoUpdate() }}
                        disabled={profilePhoto == null}
                    >
                        {isLoadingProfilePhotoUpdate ? <Loader /> : "Save image"}
                    </button>

                    <button
                        className="btn delete"
                        onClick={e => { e.preventDefault(); handleProfilePhotoDelete() }}
                    >
                        {isLoadingProfilePhotoDelete ? <Loader /> : "Delete image"}

                    </button>
                </form>
            </Modal>
        </div>
    )
}


export default observer(Profile)
