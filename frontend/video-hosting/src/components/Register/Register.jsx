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
            setSocialLinks([...socialLinks, ""]);
        }
    };

    const removeLink = (index) => {
        const newLinks = socialLinks.filter((_, i) => i !== index);
        setSocialLinks(newLinks);
    };

    const normalizeURL = (url) => {
        console.log(url)
        return url.startsWith("http://") || url.startsWith("https://")
            ? url
            : `https://${url}`;
    }

    const validateURL = (input) => {
        try {
            const urlRegex = /^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[^\s]*)?$/i;
            const normalizedUrl = normalizeURL(input);
            new URL(normalizedUrl)
            return true && urlRegex.test(normalizedUrl);
        } catch {
            return false;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {

            for (const index in socialLinks) {
                console.log(socialLinks[index])

                if (!validateURL(socialLinks[index])) {
                    setIsLoading(false);
                    alertsContext.addAlert({
                        text: "Wrong URL format",
                        time: 2000,
                        type: "error"
                    })
                    return;
                }
            }

            const normalizedLinks = socialLinks.map(link => normalizeURL(link))

            await store.register(
                {
                    username: username.trim(),
                    email: email.trim(),
                    password,
                    about: about.trim(),
                    social_links: normalizedLinks
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
            console.log(e?.response?.data?.detail);
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
                                        type="text"
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

                <label className="personal-data">
                    <input
                        name="pd"
                        type="checkbox"
                        required
                    />
                    <span>
                        I give my consent to the <a
                            href="https://docs.google.com/document/d/1m1A20bzgjTdR2st3fbih2tmDRTAFXeKo/edit?usp=sharing&ouid=107274676406622214896&rtpof=true&sd=true"
                            target="_blank"
                        >
                            processing of personal data
                        </a>
                    </span>
                </label>

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