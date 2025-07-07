from server.schemas.article_search import SearchArticleRequest
from server.services.user_service import UserService

class UserController:
    def __init__(self):
        self.service = UserService()

    def get_current_user_info(self, user_id):
        return self.service.get_user_by_id(user_id)

    def get_today_headlines(self, user_id):
        return self.service.get_headlines_today(user_id)

    def get_headlines_by_date_range(self,user_id, start_date, end_date, category=None):
        return self.service.get_headlines_in_date_range(user_id, start_date, end_date, category)

    def get_saved_articles(self, user_id):
        return self.service.get_saved_articles(user_id)

    def save_article(self, user_id, article_id):
        return self.service.save_article(user_id, article_id)

    def delete_article(self, user_id, article_id):
        return self.service.delete_article(user_id, article_id)

    # def search_articles(self, query, start_date, end_date, user_id):
    #     return self.service.search_articles(query, start_date, end_date, user_id)

    def search_articles(self, search_request: SearchArticleRequest, user_id):
        return self.service.search_articles(search_request, user_id)

    def logout(self, user_id):
        return self.service.logout(user_id)
