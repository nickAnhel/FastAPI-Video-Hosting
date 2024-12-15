import { useState } from "react";


export default function useShareModal() {
    const [isActive, setIsActive] = useState(false);
    const [link, setLink] = useState("")

    return {
        isActive,
        link,
        setIsActive,
        setLink,
    }
}