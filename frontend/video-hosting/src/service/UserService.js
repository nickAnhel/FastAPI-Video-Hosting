import api from "../http";


export default class UserService {
    static async getMe() {
        return api.get("/users/me");
    }

    static async getUserById(userId) {
        return api.get("/users/", { params: {id: userId} });
    }

    static async updateMe(data) {
        return api.put("/users/", data);
    }

    static async deleteMe() {
        return api.delete("/users/");
    }

    static async updateProfilePhoto(formData) {
        return api.put("/users/photo/", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            }
        });
    }

    static async deleteProfilePhoto() {
        return api.delete("/users/photo/")
    }

    static async getUsers(params) {
        return api.get("/users/list", { params });
    }

    static async searchUsers(params) {
        return api.get(
            "/users/search",
            { params },
        )
    }

    static async subscribeToUser(userId) {
        return api.post(`/users/subscribe?user_id=${userId}`);
    }

    static async unsubscribFromuser(userId) {
        return api.delete(`/users/unsubscribe?user_id=${userId}`);
    }

    static async getSubsctiptions(params) {
        return api.get(
            "/users/subscriptions",
            { params }
        );
    }
}