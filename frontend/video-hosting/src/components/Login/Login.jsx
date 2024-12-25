import { useState, useContext, useRef, useEffect } from "react"
import { observer } from "mobx-react-lite";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css"

import { Context } from "../../main";
import { AlertsContext } from "../../App";
import Loader from "../Loader/Loader";


const Login = () => {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const navigate = useNavigate();

    const [isLoading, setIsLoading] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const usernameInputRef = useRef(null);

    useEffect(() => {
        if (username === "") {
            usernameInputRef?.current?.focus();
        }
    }, [username])

    const handleSubmit = async (e) => {
        setIsLoading(true);
        e.preventDefault();

        try {
            await store.login(username, password);
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
        <div className="login">
            <h1>Sign In</h1>

            <form className="login-form" onSubmit={(e) => { handleSubmit(e); }}>

                <input
                    ref={usernameInputRef}
                    id="username"
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />


                <input
                    id="password"
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button
                    type="submit"
                    disabled={isLoading}
                >
                    { isLoading ? <Loader /> : "Sign In"}
                </button>
                <div className="hint">Don't have an account? <Link to="/register">Sign Up</Link></div>
            </form>
        </div>
    )
}

export default observer(Login)
