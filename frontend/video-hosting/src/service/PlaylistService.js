import api from "../http";


export default class PlaylistService {
    static async getPlaylists(params) {
        return api.get(
            "/playlists/list",
            { params }
        );
    }

    static async searchPlaylists(params) {
        return api.get(
            "/playlists/search",
            { params },
        )
    }

    static async getPlaylistById(playlistId) {
        return api.get(
            "/playlists/",
            { params: {playlist_id: playlistId} }
        )
    }

    static async createPlaylist(data) {
        return api.post("/playlists/", data)
    }

    static async deletePlylistById(playlistId) {
        return api.delete(
            "/playlists/",
            { params: { playlist_id: playlistId } }
        )
    }

    static async addVideoToPlaylist(videoId, playlistId) {
        return api.post(
            `/playlists/add-video?video_id=${videoId}&playlist_id=${playlistId}`,
        )
    }

    static async removeVideoFromPlaylist(videoId, playlistId) {
        return api.delete(
            "/playlists/remove-video",
            { params: { video_id: videoId, playlist_id: playlistId } }
        )
    }

    static async getUserPlaylistExcludeVideo(videoId) {
        return api.get(
            "/playlists/exclude-video",
            { params: { video_id: videoId } }
        )
    }
}