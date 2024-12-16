import { useState } from "react"
import { useNavigate } from "react-router-dom";
import Select from "react-select";
import "./Search.css"


function Search() {
    const navigate = useNavigate();

    const [query, setQuery] = useState("");
    const [searchScope, setSearchScope] = useState("videos");

    const [isShowSelect, setIsShowSelect] = useState(false);

    const scopeOptions = [
        { value: "videos", label: "Videos" },
        { value: "playlists", label: "Playlists" },
        { value: "channels", label: "Channels" },
    ]

    const handlePressEnter = (e) => {
        if (e.key == "Enter" && query) {
            navigate(`/search?query=${query}&scope=${searchScope}`)
        }
    }

    const handleSearch = () => {
        if (query) {
            navigate(`/search?query=${query}&scope=${searchScope}`)
        }
    }

    const handleClear = () => {
        setQuery("");
        document.getElementById("search-input").focus();
    }

    const handleChangeScope = (e) => {
        setSearchScope(e.value);

        if (query && window.location.pathname == "/search") {
            navigate(`/search?query=${query}&scope=${e.value}`)
        }
    }

    const selectStyles = {
        control: (provided, state) => ({
            // ...provided,
            transition: "all .2s",
            color: "#fff",
            width: "10rem",
            height: "2rem",
            display: "flex",
            fontSize: "1rem",
            borderRadius: "2rem",
            padding: "0 .5rem",
            backgroundColor: "#474747",
            // border: "1px solid #cecece",
            boxShadow: "none",
            outLine: "none",
            cursor: "pointer",
            opacity: state.isFocused ? ".8" : "1",
            fontWeight: "600",
        }),
        menu: (provided) => ({
            ...provided,
            borderRadius: "1rem",
            padding: ".3rem .5rem",
            backgroundColor: "#333",
        }),
        option: (provided, state) => ({
            ...provided,
            borderRadius: ".5rem",
            color: "#cecece",
            transition: "all .2s",
            padding: "0.3rem 1rem",
            backgroundColor:
                state.isFocused ? "#444" :
                    state.isSelected ? "#444" : "#333",

            cursor: state.isFocused ? "pointer" : "default",
        }),
        menuList: styles => ({
            ...styles,
            display: "flex",
            flexDirection: "column",
            gap: ".3rem",
        }),
        singleValue: provided => ({
            ...provided,
            color: "#cecece"
        }),
        dropdownIndicator: (provided, state) => ({
            ...provided,
            color: state.isFocused ? "#cecece" : "#cecece",
        }),
    }

    return (
        <div
            className="search"
            onFocus={() => setIsShowSelect(true)}
            onBlur={() => setIsShowSelect(false)}
        >
            <Select
                className={(isShowSelect || window.location.pathname == "/search" || query) ? "select" : "select hidden"}
                options={scopeOptions}
                isSearchable={false}
                defaultValue={scopeOptions[0]}
                styles={selectStyles}
                onChange={handleChangeScope}
                components={{ IndicatorSeparator: null }}
            />

            <div className="search-bar">
                <input
                    id="search-input"
                    type="text"
                    placeholder="Search"
                    value={query}
                    maxLength={50}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handlePressEnter}

                />
                <div className="search-actions">
                    <button
                        className={query ? "show search-btn" : "search-btn hidden"}
                        onClick={handleClear}
                        disabled={!query}
                    >
                        <img
                            className="close"
                            src="../../../assets/clear.svg"
                            alt="Clear"
                        />
                    </button>
                    <button
                        className="search-btn"
                        disabled={!query}
                    >
                        <img
                            src="../../../assets/search.svg"
                            alt="Search"
                            onClick={handleSearch}
                        />
                    </button>
                </div>

            </div>

        </div>
    )
}

export default Search