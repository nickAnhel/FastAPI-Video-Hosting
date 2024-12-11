import api from "../http";


export default class CommentService {
    static async getComments(params) {
        return api.get(
            "/comments/list",
            { params }
        );
    }

    static async createComment(videoId, content) {
        return api.post(
            "/comments/",
            {
                video_id: videoId,
                content: content,
            }
        );
    }

    static async deleteComment(commentId) {
        return api.delete(
            "/comments/",
            { params: {
                comment_id: commentId
            }}
        );
    }
}