import { useState, useContext } from "react";
import "./ShareModal.css"

import { ShareModalContext } from "../../App";
import Modal from "../Modal/Modal";


function ShareModal() {
    const shareModalContext = useContext(ShareModalContext);
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = () => {
        setIsCopied(true);
        navigator.clipboard.writeText(shareModalContext.link);
        setTimeout(() => {
            setIsCopied(false);
        }, 3000)
    }

    return (
        <Modal
            active={shareModalContext.isActive}
            setActive={shareModalContext.setIsActive}
        >
            <div className="share">
                <div className="share-link">{shareModalContext.link}</div>
                <button
                    className={isCopied ? "copy-btn copied" : "copy-btn"}
                    onClick={handleCopy}
                >
                    {isCopied ? "Copied" : "Copy"}
                </button>
            </div>
        </Modal>
    )
}

export default ShareModal;