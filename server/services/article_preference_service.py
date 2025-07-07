from server.repos.article_preference_repo import ArticlePreferenceRepo
from server.Exceptions.article_exceptions import ArticleNotFoundException

class ArticlePreferenceService:
    def __init__(self):
        self.repo = ArticlePreferenceRepo()

    def like_article(self, user_id, article_id):
        result = self.repo.set_preference(user_id, article_id, 'like')
        if not result:
            raise ArticleNotFoundException(f"Failed to like article {article_id} for user {user_id}")
        return result

    def dislike_article(self, user_id, article_id):
        result = self.repo.set_preference(user_id, article_id, 'dislike')
        if not result:
            raise ArticleNotFoundException(f"Failed to dislike article {article_id} for user {user_id}")
        return result