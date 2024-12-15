import { useState, useRef, useEffect, useContext } from "react"
import "./Options.css"

import { OptionsContext } from "../../App";
import Option from "../Option/Option";


function Options({ itemId }) {
    const optionsContext = useContext(OptionsContext);

    const [isOpen, setIsOpen] = useState(false);
    const [menuTopValue, setMenuTopValue] = useState("3rem");
    const menuRef = useRef(null);

    const handleToggleMenu = (event) => {
        event.stopPropagation();
        event.preventDefault();

        if (!isOpen) {
            updateMenuTopValue();
            setIsOpen(!isOpen);
        } else {
            setIsOpen(!isOpen);
        }
    };

    const handleClickOutside = (event) => {
        if (menuRef.current && !menuRef.current.contains(event.target)) {
            setIsOpen(false);
        }
    };

    useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    const updateMenuTopValue = () => {
        try {
            const menu = document.getElementById(itemId)
            const rect = menu.getBoundingClientRect();

            if (window.innerHeight - rect.bottom < 150) {
                setMenuTopValue(`-${optionsContext.options.length * 3 + (optionsContext.options.length - 1) * 0.5 + 1.5}rem`);
            } else {
                setMenuTopValue("3rem")
            }
        } catch (e) {
            console.log(e);
        }
    }

    useEffect(() => {
        updateMenuTopValue();
    }, [itemId])

    const handleClick = (e, handler, params) => {
        e.preventDefault();
        setIsOpen(!isOpen);

        if (params) {
            handler(itemId, params);
        } else {
            handler(itemId);
        }
    }

    return (
        <div className="options" ref={menuRef}>
            <img
                className="options-btn"
                src="../../../../assets/options.svg"
                alt="Options"
                onClick={handleToggleMenu}
            />

            <div
                id={itemId}
                className={isOpen ? "options-menu active" : "options-menu"}
                style={{ top: menuTopValue }}
            >
                {
                    optionsContext.options.map((option, index) => {
                        return <Option
                            key={`${itemId}-${index}`}
                            text={option.text}
                            iconSrc={option.iconSrc}
                            onClickHandler={(e) => handleClick(e, option.actionHandler, option.params)}
                        />
                    })
                }
            </div>
        </div>
    );
}

export default Options;