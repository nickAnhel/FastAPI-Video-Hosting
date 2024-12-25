import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import "./CreateVideo.css";

import { Context } from "../../main";
import { AlertsContext } from "../../App";
import VideoService from "../../service/VideoService";
import Loader from "../Loader/Loader";
import Unauthorized from "../Unauthorized/Unauthorized";


function CreateVideo() {
    const { store } = useContext(Context);
    const alertsContext = useContext(AlertsContext);
    const navigate = useNavigate();

    const [isLoading, setIsLoading] = useState(false);

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [preview, setPreview] = useState(null);
    const [video, setVideo] = useState(null);

    const [previewFileSrc, setPreviewFileSrc] = useState(null);
    const [videoFileSrc, setVideoFileSrc] = useState(null);

    const handleSelectFile = (e, setFileSrc) => {
        if (!e.target.files || e.target.files.length === 0) {
            setFileSrc(null);
            return
        }

        const objectUrl = URL.createObjectURL(e.target.files[0]);
        setFileSrc(objectUrl);
    }

    const handlePublish = async () => {
        if (video.size > 1000000000) {
            alertsContext.addAlert({
                text: "Video size is too large",
                time: 2000,
                type: "error"
            })
            return;
        }

        if (preview.size > 10000000) {
            alertsContext.addAlert({
                text: "Preview size is too large",
                time: 2000,
                type: "error"
            })
            return;
        }

        alertsContext.addAlert({
            text: "Video is publishing. Do not leave this page!",
            time: 5000,
            type: "success"
        })

        const videoData = {
            video: video,
            preview: preview,
            title: title,
            description: description
        }

        setIsLoading(true);

        try {
            await VideoService.createVideo(videoData);
            alertsContext.addAlert({
                text: "Successfully published video",
                time: 2000,
                type: "success"
            })
            navigate("/");
        } catch (e) {
            console.log(e);
            alertsContext.addAlert({
                text: "Failed to publish video",
                time: 2000,
                type: "error"
            })
        }

        setIsLoading(false);
    }

    if (!store.isAuthenticated) {
        return <Unauthorized />
    }

    return (
        <div className="create-video">
            <div className="video-files">
                <label
                    htmlFor="preview-file"
                    className="file"
                >
                    <div hidden={preview} >Select preview</div>

                    <img
                        className="preview"
                        src={previewFileSrc}
                    />
                    <input
                        className="file-input"
                        type="file"
                        id="preview-file"
                        accept=".png, .jpg, .jpeg"
                        onChange={e => {
                            setPreview(e.target.files[0]);
                            handleSelectFile(e, setPreviewFileSrc);
                        }}
                    />
                </label>

                <label
                    htmlFor="video-file"
                    className="file"
                // style={{boxShadow: video ? "" :  "inset 0 0 2rem 1rem rgba(0, 0, 0, .2)",}}
                >
                    <div hidden={video} >Select video</div>
                    <video
                        className="video"
                        src={videoFileSrc}
                        autoPlay
                        loop
                        controls
                        muted
                    />
                    <input
                        className="file-input"
                        type="file"
                        id="video-file"
                        accept=".mp4"
                        onChange={e => {
                            setVideo(e.target.files[0]);
                            handleSelectFile(e, setVideoFileSrc);
                        }}
                    />
                </label>
            </div>

            <div className="video-info">
                <input
                    className="video-title"
                    type="text"
                    value={title}
                    maxLength={100}
                    placeholder="Video Title"
                    onChange={(e) => setTitle(e.target.value)}
                    style={{ borderColor: title.trim() ? "#fff" : "#7e7e7e" }}
                />


                <div
                    className="video-desc-wrapper"
                    style={{ borderColor: description.trim() ? "#fff" : "#7e7e7e" }}
                >
                    <textarea
                        className="video-desc"
                        value={description}
                        maxLength={255}
                        placeholder="Video Description"
                        onChange={(e) => setDescription(e.target.value)}
                    ></textarea>
                    <span className="video-desc-length">{description.trim().length} / 255</span>
                </div>


                <button
                    className="publish"
                    onClick={handlePublish}
                    disabled={!title.trim() || !description.trim() || !preview || !video}
                >
                    {isLoading ? <Loader /> : "Publish Video"}
                </button>
            </div>
        </div>
    )
}

export default CreateVideo;