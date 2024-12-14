import api from "../http";


export default class PlaylistService {
    static async getPlaylists(params) {
        return api.get(
            "/playlists/list",
            { params }
        );
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
}