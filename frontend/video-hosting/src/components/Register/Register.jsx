import { useState, useContext } from "react"
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import "./Register.css"

import { Context } from "../../main";
import { AlertsContext } from "../../App";
import Loader from "../Loader/Loader";


function Register() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [about, setAbout] = useState("");
    const [socialLinks, setSocialLinks] = useState([]);

    const [isLoading, setIsLoading] = useState(false);

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

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await store.register(
                {
                    username: username.trim(),
                    email: email.trim(),
                    password,
                    about: about.trim(),
                    social_links: socialLinks
                }
            )
            navigate("/");
        } catch (e) {
            if (e.response?.data?.detail) {
                alertsContext.addAlert({
                    text: e.response?.data?.detail,
                    time: 2000,
                    type: "error"
                })
            } else {
                alertsContext.addAlert({
                    text: "Something went wrong. Please try again",
                    time: 2000,
                    type: "error"
                })
            }
            console.log(e);
            console.log(e.response?.data?.detail);
        }

        setIsLoading(false);
    }

    return (
        <div className="register">
            <h1>Sign Up</h1>

            <form
                className="register-form"
                onSubmit={(e) => { handleSubmit(e); }}
            >
                <div className="form-part">
                    <h3>Your credentials</h3>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        maxLength={50}
                        required
                    />
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        minLength={8}
                        maxLength={50}
                        required
                    />
                </div>

                <div className="form-part">
                    <h3>Tell people about your channel</h3>
                    <div className="about-wrapper">
                        <textarea
                            className="about"
                            rows={5}
                            placeholder="About"
                            value={about}
                            onChange={(e) => setAbout(e.target.value)}
                            maxLength={255}
                        ></textarea>
                        <span className="about-length">{about.trim().length} / 255</span>
                    </div>
                </div>

                <div className="form-part">
                    <h3>Add social links</h3>
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

                <button
                    type="submit"
                    disabled={isLoading}
                >
                    {isLoading ? <Loader /> : "Sign Up"}
                </button>
            </form>

        </div>
    )
}

export default observer(Register)