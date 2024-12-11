import { Link } from "react-router-dom";
import "./NotFound.css";


function NotFound() {
    return (
        <div className="not-found">
            <h1>404</h1>
            <p>Page not found. <Link to={"/"}>Return to main page</Link></p>
        </div>
    );
}

export default NotFound;
