from app.comments.repository import CommentRepository


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository
