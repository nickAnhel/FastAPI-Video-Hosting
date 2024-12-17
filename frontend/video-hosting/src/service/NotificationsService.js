import api from "../http";


export default class NotificationsService {
    static async getNotifications(params) {
        return api.get(
            "/notifications/",
            { params },
        )
    }

    static async getNewNotificationsCount() {
        return api.get("/notifications/new")
    }

    static async deleteNotificationById(notificationId) {
        return api.delete(`/notifications/?notification_id=${notificationId}`)
    }
}