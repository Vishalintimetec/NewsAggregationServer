import requests
from server.schemas.news import NewsArticleCreate
from server.repos.news_repository import NewsRepository
from server.repos.category_repo import CategoryRepo
from server.repos.external_api_repo import ExternalAPIRepository
from server.config.constants import API_URL
from server.utils.category_classifier import CategoryClassifier
from server.services.newsapi_service import NewsAPIService
from server.services.thenewsapi_service import TheNewsAPIService
from server.services.api_manager import APIManager
from server.services.notification_service import NotificationService


class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()
        self.api_manager = APIManager()
        self.category_repo = CategoryRepo()
        self.classifier = CategoryClassifier()
        self.newsapi_service = NewsAPIService()
        self.thenewsapi_service = TheNewsAPIService()
        self.notification_service = NotificationService()


    def get_active_api(self):
        return self.api_manager.get_active_api()

    def fetch_news(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
        return None

    def fetch_news_from_api(self):
        print("Starting sync from external API...")

        active_api = self.get_active_api()
        if not active_api:
            return {"error": "No active external APIs available"}

        api_url = API_URL.get(active_api["server_name"])
        api_key = active_api["api_key"]
        server_id = active_api["server_id"]

        full_url = api_url + api_key
        print(f"Fetching news from {full_url}")

        data = self.fetch_news(full_url)
        if not data:
            return {"error": f"Failed to fetch news from {active_api['server_name']}"}

        if "thenewsapi" in api_url.lower():
            articles = self.thenewsapi_service.fetch_news_articles({
                "api_url": api_url,
                "api_key": api_key,
                "server_id": server_id
            })
        else:
            articles = self.newsapi_service.fetch_news_articles({
                "api_url": api_url,
                "api_key": api_key,
                "server_id": server_id
            })

        saved_count = 0
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",articles)
        for article in articles:
            print(article)
            article_id = self.news_repo.save(article)

            for category_name in article.categories:
                print(category_name)
                if category_name:
                    category = self.category_repo.get_category_by_name(category_name)
                    print("kkkkkkkkkkkkk",category)

                    if category:
                        category_id = category["category_id"]
                    else:
                        category_name = CategoryClassifier.DEFAULT_CATEGORY
                        default_category = self.category_repo.get_id_by_name(category_name)
                        category_id = default_category["category_id"] if default_category else None

                    if category_id:
                        self.category_repo.insert_article_category(category_id, article_id)
                        print(f"Mapped Article {article_id} to Category '{category_name}'")

            saved_count += 1
        self.notification_service.generate_notifications_for_new_articles()
        self.notification_service.send_unread_notifications()
        print(f"{saved_count} articles stored from {active_api['server_name']}")
        return {
            "message": f"{saved_count} articles stored from {active_api['server_name']}",
            "source": active_api["server_name"]
        }
