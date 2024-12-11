import api from "../http";


export default class AuthService {
    static async register(data) {
        return api.post("/users/", data);
    }

    static async login(username, password) {
        return api.post("/auth/token", `grand_type=password&username=${username}&password=${password}`)
    }

    static async logout() {
        return api.post("/auth/logout");
    }
}