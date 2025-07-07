import requests
from server.schemas.news import NewsArticleCreate
from server.utils.logger import logger
from server.repos.news_repository import NewsRepository
from server.repos.category_repo import CategoryRepo
from server.config.constants import API_URL
from server.utils.category_classifier import CategoryClassifier
from server.services.api_manager import APIManager
from server.services.notification_service import NotificationService
from server.services.factories.external_api_service_factory import ExternalAPIServiceFactory


class NewsService:
    def __init__(self):
        self.news_repo = NewsRepository()
        self.api_manager = APIManager()
        self.category_repo = CategoryRepo()
        self.classifier = CategoryClassifier()
        self.notification_service = NotificationService()

    def fetch_news(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            logger.info(f"Error fetching news: {e}")
        return None

    def fetch_news_from_api(self):
        print("Starting sync from external APIs...")
        apis = self.api_manager.get_all_server_details()
        for api in apis:
            api_url = API_URL.get(api["server_name"])
            api_key = api["api_key"]
            server_id = api["server_id"]
            full_url = api_url + api_key
            print(f"Trying to fetch news from {full_url}")
            data = self.fetch_news(full_url)
            if not data:
                print(f"Failed to fetch news from {api['server_name']}, trying next API...")
                continue
            api_service = ExternalAPIServiceFactory.get_service(api["server_name"])
            articles = api_service.fetch_news_articles({
                "api_url": api_url,
                "api_key": api_key,
                "server_id": server_id
            })
            if articles:
                print(f"Fetched {len(articles)} articles from {api['server_name']}")
                saved_count = 0
                for article in articles:
                    article_id = self.news_repo.save(article)
                    for category_name in article.categories:
                        if category_name:
                            category = self.category_repo.get_category_by_name(category_name)
                            if category:
                                category_id = category["category_id"]
                            else:
                                category_name = CategoryClassifier.DEFAULT_CATEGORY
                                default_category = self.category_repo.get_category_id_by_name(category_name)
                                category_id = default_category["category_id"] if default_category else None
                            if category_id:
                                self.category_repo.insert_article_category(category_id, article_id)
                    saved_count += 1
                self.notification_service.generate_notifications_for_new_articles()
                self.notification_service.send_unread_notifications()
                print(f"{saved_count} articles stored from {api['server_name']}")
                return {
                    "message": f"{saved_count} articles stored from {api['server_name']}",
                    "source": api["server_name"]
                }
            else:
                logger.error(f"No articles found from {api['server_name']}, trying next API...")
                print(f"No articles found from {api['server_name']}, trying next API...")
        return {"error": "Failed to fetch news from all available APIs"}
