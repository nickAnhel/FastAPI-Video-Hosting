import { useState } from "react";


export default function useAddVideoModal() {
    const [active, setActive] = useState(false);
    const [videoId, setVideoId] = useState(null)

    return {
        active,
        videoId,
        setActive,
        setVideoId,
    }
}