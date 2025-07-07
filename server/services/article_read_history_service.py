from server.repos.article_read_history_repo import ReadHistoryRepo
from server.Exceptions.article_exceptions import ArticleNotFoundException

class ArticleReadHistoryService:
    def __init__(self):
        self.repo = ReadHistoryRepo()

    def record_read(self, user_id, article_id):
        result = self.repo.add_read_history(user_id, article_id)
        if not result:
            raise ArticleNotFoundException(f"Failed to record read history for article {article_id} and user {user_id}")
        return result

    def get_read_history(self, user_id):
        history = self.repo.get_read_history(user_id)
        if not history:
            raise ArticleNotFoundException(f"No read history found for user {user_id}")
        return history