import api from "../http";


export default class VideoService {
    static async createVideo(data) {
        return api.post(
            "/videos/",
            data,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            }
        )
    }

    static async getVideos(params) {
        return api.get(
            "/videos/list",
            { params }
        );
    }

    static async getHistory(params) {
        return api.get(
            "/videos/history",
            { params }
        )
    }

    static async clearHistory() {
        return api.delete("/videos/history/clear")
    }

    static async getLiked(params) {
        return api.get(
            "/videos/liked",
            { params }
        )
    }

    static async getVideoById(videoId) {
        return api.get(
            "/videos/",
            { params: { video_id: videoId } }
        )
    }

    static async addView(videoId) {
        return api.patch(
            `/videos/add-view?video_id=${videoId}`
        )
    }

    static async likeVideo(videoId) {
        return api.post(
            `/videos/like?video_id=${videoId}`
        )
    }

    static async unlikeVideo(videoId) {
        return api.delete(
            `/videos/like?video_id=${videoId}`
        )
    }

    static async dislikeVideo(videoId) {
        return api.post(
            `/videos/dislike?video_id=${videoId}`
        )
    }

    static async undislikeVideo(videoId) {
        return api.delete(
            `/videos/dislike?video_id=${videoId}`
        )
    }

    static async getSubscriptions(params) {
        return api.get(
            "/videos/subscriptions",
            { params }
        )
    }

    static async getPlaylistVideos(params) {
        return api.get(
            "/videos/playlist",
            { params }
        )
    }
}