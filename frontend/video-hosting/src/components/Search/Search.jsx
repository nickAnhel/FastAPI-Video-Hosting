import { useState } from "react"
import "./Search.css"


function Search() {
    const [query, setQuery] = useState("");

    return (
        <div className="search">
            <input
                type="text"
                placeholder="Search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <img
                src="../../../assets/search.svg"
                alt="Search"

            />
        </div>
    )
}

export default Search