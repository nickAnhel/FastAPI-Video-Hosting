import api from "../http";


export default class VideoService {
    static async getVideos(params) {
        return api.get(
            "/videos/list",
            { params }
        );
    }
}