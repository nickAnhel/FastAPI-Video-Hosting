import { Link } from "react-router-dom";
import "./Unauthorized.css";


function Unauthorized() {
    return (
        <div className="unauthorized">
            <h1>Unauthorized</h1>
            <p>You are not authorized to access this page. Please <Link to="/login">log in.</Link></p>
        </div>
    )
}

export default Unauthorized;