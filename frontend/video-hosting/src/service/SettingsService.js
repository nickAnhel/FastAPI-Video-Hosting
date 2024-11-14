import api from "../http"


export default class SettingsService {
    static async getSettings() {
        return api.get('/settings/');
    }

    static async updateSettings(data) {
        return api.put('/settings/', data);
    }
}
