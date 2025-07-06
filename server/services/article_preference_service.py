from server.repos.article_preference_repo import ArticlePreferenceRepo

class ArticlePreferenceService:
    def __init__(self):
        self.repo = ArticlePreferenceRepo()

    def like_article(self, user_id, article_id):
        return self.repo.set_preference(user_id, article_id, 'like')

    def dislike_article(self, user_id, article_id):
        return self.repo.set_preference(user_id, article_id, 'dislike')