from server.services.article_preference_service import ArticlePreferenceService

class ArticlePreferenceController:
    def __init__(self):
        self.service = ArticlePreferenceService()

    def like_article(self, user_id, article_id):
        return self.service.like_article(user_id, article_id)

    def dislike_article(self, user_id, article_id):
        return self.service.dislike_article(user_id, article_id)