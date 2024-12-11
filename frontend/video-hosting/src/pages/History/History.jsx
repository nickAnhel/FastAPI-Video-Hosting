import { useState } from "react";
import "./History.css"

import VideoService from "../../service/VideoService";
import VideosList from "../../components/VideosList/VideosList";


function History() {
    const [clear, setClear] = useState(false);

    const handleClearHistory = async () => {
        await VideoService.clearHistory();
        setClear((prev) => !prev);
    }

    return (
        <div className="history-page">
            <VideosList fetchVideos={VideoService.getHistory} filters={{desc: true}} clear={clear} />
            <button
                className="clear"
                onClick={handleClearHistory}
            >
                Clear
            </button>
        </div>
    )
}

export default History;