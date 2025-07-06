from server.repos.article_read_history_repo import ReadHistoryRepo

class ArticleReadHistoryService:
    def __init__(self):
        self.repo = ReadHistoryRepo()

    def record_read(self, user_id, article_id):
        return self.repo.add_read_history(user_id, article_id)

    def get_read_history(self, user_id):
        return self.repo.get_read_history(user_id)