import api from "../http";


export default class UserService {
    static async getMe() {
        return api.get("/users/me");
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
}