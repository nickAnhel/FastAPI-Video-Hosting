import { useState, useContext } from "react"
import { observer } from "mobx-react-lite";
import { Link, useNavigate } from "react-router-dom";
import "./Login.css"

import { Context } from "../../main";


const Login = () => {
    const { store } = useContext(Context);
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await store.login(username, password);
            navigate("/");
        } catch (e) {
            setError(e.response?.data?.detail);
            console.log(e.response?.data?.detail);
        }
    }

    return (
        <div className="login">
            <h1>Sign In</h1>

            <form className="login-form" onSubmit={(e) => { handleSubmit(e); }}>

                <input
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

                {error && <div className="error">{error}</div>}

                <button type="submit">
                    Sign In
                </button>
                <div className="hint">Don't have an account? <Link to="/register">Sign Up</Link></div>
            </form>
        </div>
    )
}

export default observer(Login)
