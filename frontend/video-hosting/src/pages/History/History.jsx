import { useState, useContext } from "react";
import "./History.css"

import { Context } from "../../main";
import VideoService from "../../service/VideoService";
import Unauthorized from "../../components/Unauthorized/Unauthorized";
import VideosList from "../../components/VideosList/VideosList";


function History() {
    const { store } = useContext(Context);
    const [clear, setClear] = useState(false);

    const handleClearHistory = async () => {
        await VideoService.clearHistory();
        setClear((prev) => !prev);
    }

    if (!store.isAuthenticated) {
        return (
            <div className="history-page">
                <Unauthorized />
            </div>
        )
    }

    return (
        <div className="history-page">
            <VideosList fetchVideos={VideoService.getHistory} filters={{ desc: true }} clear={clear} />
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