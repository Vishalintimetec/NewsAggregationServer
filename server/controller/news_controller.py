from server.services.news_service import NewsService

class NewsController:
    def __init__(self):
        self.news_service = NewsService()

    def fetch_news(self):
        return self.news_service.fetch_news_from_api()