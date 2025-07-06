from server.services.article_read_history_service import ArticleReadHistoryService

class ArticleReadHistoryController:
    def __init__(self):
        self.read_history_service = ArticleReadHistoryService()

    def record_read(self, user_id, article_id):
        return self.read_history_service.record_read(user_id, article_id)

    def get_read_history(self, user_id):
        return self.read_history_service.get_read_history(user_id)